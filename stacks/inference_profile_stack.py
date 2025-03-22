from aws_cdk import (
    Stack,
    aws_bedrock as bedrock,
    aws_ssm as ssm,
    CfnTag,
)
from constructs import Construct

class InferenceProfileStack(Stack):

    def __init__(self, scope: Construct, id: str, travel_model_arn: str, insurance_model_arn: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Travel ChatBot Inference Profile
        travel_chatbot_profile = bedrock.CfnApplicationInferenceProfile(
            self, "TravelChatBotInferenceProfile",
            inference_profile_name=f"{self.stack_name}-TravelChatBot",
            description="Inference profile for the Travel ChatBot.",
            model_source=bedrock.CfnApplicationInferenceProfile.InferenceProfileModelSourceProperty(
                copy_from=travel_model_arn
            ),
            tags=[
                CfnTag(
                    key="Application",
                    value="TravelChatBot"
                ),
                CfnTag(
                    key="CostCenter",
                    value="Travel"
                )
            ]
        )

        # Insurance ChatBot Inference Profile
        insurance_chatbot_profile = bedrock.CfnApplicationInferenceProfile(
            self, "InsuranceChatBotInferenceProfile",
            inference_profile_name=f"{self.stack_name}-InsuranceChatBot",
            description="Inference profile for the Insurance ChatBot.",
            model_source=bedrock.CfnApplicationInferenceProfile.InferenceProfileModelSourceProperty(
                copy_from=insurance_model_arn
            ),
            tags=[
                CfnTag(
                    key="Application",
                    value="InsuranceChatBot"
                ),
                CfnTag(
                    key="CostCenter",
                    value="Insurance"
                )
            ]
        )

        # SSM Parameters
        # ssm.StringParameter(
        #     self, "TravelChatBotParameter",
        #     parameter_name="/bedrock/inference-profiles/TravelChatBot",
        #     description="ARN for the TravelChatBot inference profile.",
        #     string_value=travel_chatbot_profile.ref,
        #     tags={
        #         "Application": "TravelChatBot",
        #         "CostCenter": "Travel"
        #     }
        # )

        # ssm.StringParameter(
        #     self, "InsuranceChatBotParameter",
        #     parameter_name="/bedrock/inference-profiles/InsuranceChatBot",
        #     description="ARN for the InsuranceChatBot inference profile.",
        #     string_value=insurance_chatbot_profile.ref,
        #     tags={
        #         "Application": "InsuranceChatBot",
        #         "CostCenter": "Insurance"
        #     }
        # )