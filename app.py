from aws_cdk import App
from config import EnvSettings, KbConfig, OpenSearchServerlessConfig
from stacks.s3_stack import S3Stack
from stacks.kb_role_stack import KbRoleStack
from stacks.oss_infra_stack import OpenSearchServerlessInfraStack
from stacks.lambda_stack import LambdaStack
from stacks.kb_infra_stack import KbInfraStack

app = App()

# create S3 bucket  
s3_stack = S3Stack(app, "S3Stack")

# create IAM role for kb
kb_role_stack = KbRoleStack(
    app, 
    "KbRoleStack",
    account_id=EnvSettings.ACCOUNT_ID,
    region=EnvSettings.ACCOUNT_REGION,
    kb_role_name=KbConfig.KB_ROLE_NAME,
    bucket_name=s3_stack.bucket_name
)

# setup OSS
oss_stack = OpenSearchServerlessInfraStack(
    app, 
    "OpenSearchServerlessInfraStack"
)

# create Lambda function
lambda_stack = LambdaStack(app, "LambdaStack")

# create Knowledgebase and datasource
KbInfraStack(
    app, 
    "KbInfraStack",
    bucket_name=s3_stack.bucket_name,
    weather_lambda=lambda_stack
)
app.synth()
