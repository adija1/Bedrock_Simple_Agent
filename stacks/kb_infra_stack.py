import json 
from constructs import Construct

import aws_cdk as core
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_ssm as ssm,
    aws_events as events,
)

from aws_cdk import aws_bedrock as bedrock

from aws_cdk.aws_bedrock import (
  CfnKnowledgeBase,
  CfnDataSource
)

from config import EnvSettings, KbConfig, OpenSearchServerlessConfig

region = EnvSettings.ACCOUNT_REGION
account_id = EnvSettings.ACCOUNT_ID

collectionName = OpenSearchServerlessConfig.COLLECTION_NAME
indexName = OpenSearchServerlessConfig.INDEX_NAME

import json 
embeddingModelId = KbConfig.EMBEDDING_MODEL_ID
agentModelId = KbConfig.AGENT_MODEL_ID
max_tokens = KbConfig.MAX_TOKENS
overlap_percentage = KbConfig.OVERLAP_PERCENTAGE
agentInstruction = KbConfig.AGENT_INSTRUCTION
class KbInfraStack(Stack):

    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        weather_lambda: lambda_.Function,
        bucket_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.bucket_name = bucket_name
        self.embeddingModelId = embeddingModelId

        # Get the partition dynamically
        partition = Stack.of(self).partition

        # Construct ARNs using the correct partition
        self.embedding_model_arn = f"arn:{partition}:bedrock:{region}::foundation-model/{embeddingModelId}"
        self.s3_bucket_arn = f"arn:{partition}:s3:::{self.bucket_name}"

        self.kbRoleArn = ssm.StringParameter.from_string_parameter_attributes(
            self, 
            "kbRoleArn",
            parameter_name="/e2e-rag/kbRoleArn"
        ).string_value
        
        self.collectionArn = ssm.StringParameter.from_string_parameter_attributes(
            self, 
            "collectionArn",
            parameter_name="/e2e-rag/collectionArn"
        ).string_value

        # Create Knowledgebase
        self.knowledge_base = self.create_knowledge_base()
        self.data_source = self.create_data_source(self.knowledge_base)
        
        # Create Agent
        self.agent = self.create_agent(weather_lambda)
        
    def create_knowledge_base(self) -> CfnKnowledgeBase:
        return CfnKnowledgeBase(
            self, 
            'e2eRagKB',
            knowledge_base_configuration=CfnKnowledgeBase.KnowledgeBaseConfigurationProperty(
                type="VECTOR",
                vector_knowledge_base_configuration=CfnKnowledgeBase.VectorKnowledgeBaseConfigurationProperty(
                    embedding_model_arn=self.embedding_model_arn
                )
            ),
            name='docKnowledgeBase',
            role_arn=self.kbRoleArn,
            description='e2eRAG Knowledge base',
            storage_configuration=CfnKnowledgeBase.StorageConfigurationProperty(
                type="OPENSEARCH_SERVERLESS",
                opensearch_serverless_configuration=bedrock.CfnKnowledgeBase.OpenSearchServerlessConfigurationProperty(
                    collection_arn=self.collectionArn,
                    field_mapping=bedrock.CfnKnowledgeBase.OpenSearchServerlessFieldMappingProperty(
                        metadata_field="AMAZON_BEDROCK_METADATA",
                        text_field="AMAZON_BEDROCK_TEXT_CHUNK",
                        vector_field="bedrock-knowledge-base-default-vector"
                    ),
                    vector_index_name=indexName
                )
            )
        )
  
    def create_data_source(self, knowledge_base) -> CfnDataSource:
        kbid = knowledge_base.attr_knowledge_base_id
        chunking_strategy = KbConfig.CHUNKING_STRATEGY
        
        if chunking_strategy == "Fixed-size chunking":
            vector_ingestion_config = bedrock.CfnDataSource.VectorIngestionConfigurationProperty(
                chunking_configuration=bedrock.CfnDataSource.ChunkingConfigurationProperty(
                    chunking_strategy="FIXED_SIZE",
                    fixed_size_chunking_configuration=bedrock.CfnDataSource.FixedSizeChunkingConfigurationProperty(
                        max_tokens=max_tokens,
                        overlap_percentage=overlap_percentage
                    )
                )
            )
        elif chunking_strategy == "Default chunking":
            vector_ingestion_config = bedrock.CfnDataSource.VectorIngestionConfigurationProperty(
                chunking_configuration=bedrock.CfnDataSource.ChunkingConfigurationProperty(
                    chunking_strategy="FIXED_SIZE",
                    fixed_size_chunking_configuration=bedrock.CfnDataSource.FixedSizeChunkingConfigurationProperty(
                        max_tokens=300,
                        overlap_percentage=20
                    )
                )
            )
        else:
            vector_ingestion_config = bedrock.CfnDataSource.VectorIngestionConfigurationProperty(
                chunking_configuration=bedrock.CfnDataSource.ChunkingConfigurationProperty(
                    chunking_strategy="NONE"
                )
            )

        return CfnDataSource(
            self, 
            "e2eRagDataSource",
            data_source_configuration=CfnDataSource.DataSourceConfigurationProperty(
                s3_configuration=CfnDataSource.S3DataSourceConfigurationProperty(
                    bucket_arn=self.s3_bucket_arn,
                ),
                type="S3"
            ),
            knowledge_base_id=kbid,
            name="e2eRAGDataSource",
            description="e2eRAG DataSource",
            vector_ingestion_configuration=vector_ingestion_config
        )
  
    def create_ingest_lambda(self, knowledge_base, data_source) -> lambda_:
        ingest_lambda = lambda_.Function(
            self,
            "IngestionJob",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="ingestJobLambda.lambda_handler",
            code=lambda_.Code.from_asset("./src/IngestJob"),
            timeout=Duration.minutes(5),
            environment={
                "KNOWLEDGE_BASE_ID": knowledge_base.attr_knowledge_base_id,
                "DATA_SOURCE_ID": data_source.attr_data_source_id,
            }
        )

        ingest_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:StartIngestionJob"],
                resources=[knowledge_base.knowledge_base_arn]
            )
        )
        return ingest_lambda

    def create_query_lambda(self, knowledge_base) -> lambda_:
        partition = Stack.of(self).partition
        
        query_lambda = lambda_.Function(
            self, 
            "Query",
            runtime=lambda_.Runtime.PYTHON_3_10,
            handler="queryKBLambda.handler",
            code=lambda_.Code.from_asset("./src/queryKnowledgeBase"),
            timeout=Duration.minutes(5),
            environment={
                "KNOWLEDGE_BASE_ID": knowledge_base.attr_knowledge_base_id
            }
        )

        # Function URL configuration with CORS
        fn_url = query_lambda.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.NONE,
            invoke_mode=lambda_.InvokeMode.BUFFERED,
            cors={
                "allowed_origins": ["*"],
                "allowed_methods": [lambda_.HttpMethod.POST]
            }
        )

        # Add permissions for Bedrock in GovCloud
        query_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "bedrock:RetrieveAndGenerate",
                    "bedrock:Retrieve",
                    "bedrock:InvokeModel",
                ],
                resources=[f"arn:{partition}:bedrock:{region}:*:*"]
            )
        )

        return query_lambda
  
    def add_eventbridge_rule(self, bucket, lambda_function):
        rule = events.Rule(
            self, 
            "MyRule",
            event_pattern=events.EventPattern(
                source=["aws.s3"],
                detail_type=["Object Created"],
            )
        )
        rule.add_target(lambda_function)
        bucket.grant_read(lambda_function)
        
    def get_weather_api_schema(self) -> dict:
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "Time API",
                "version": "1.0.0",
                "description": "API to get the temperature information of a city."
            },
            "paths": {
                "/get-weather-info": {
                "get": {
                    "summary": "Get the temperature information of a city.",
                    "description": "Retrieve the temperature information of a city.",
                    "operationId": "get-weather-info",
                    "parameters": [
                    {
                        "name": "city",
                        "in": "query",
                        "description": "The name of the city for which temperature information is needed.",
                        "required": True,
                        "schema": {
                        "type": "string"
                        }
                    }
                    ],
                    "responses": {
                    "200": {
                        "description": "Successful response containing the temperature information.",
                        "content": {
                        "application/json": {
                            "schema": {
                            "type": "object",
                            "properties": {
                                "temperature": {
                                "type": "string",
                                "description": "The current temperature of the city."
                                }
                            }
                            }
                        }
                        }
                    }
                    }
                }
                }
            }
        }

        
    def create_agent(self, weather_lambda):
        return bedrock.CfnAgent(
            self, "WeatherKnowledgeAgent",
            agent_name="WeatherKnowledgeAgent",
            instruction=agentInstruction,
            foundation_model=agentModelId,
            knowledge_bases=[bedrock.CfnAgent.AgentKnowledgeBaseProperty(
                description="Main knowledge base",
                knowledge_base_id=self.knowledge_base.attr_knowledge_base_id
            )],
            action_groups=[bedrock.CfnAgent.AgentActionGroupProperty(
                action_group_name="WeatherActionGroup",
                description="A Function that can access the weather data",
                action_group_executor=bedrock.CfnAgent.ActionGroupExecutorProperty(
                    lambda_=weather_lambda.weather_function_arn,
                ),
                api_schema=bedrock.CfnAgent.APISchemaProperty(
                    payload=json.dumps(self.get_weather_api_schema())
                    ),
                )],
        )