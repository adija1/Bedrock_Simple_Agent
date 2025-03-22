from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam,
    Duration
)
from constructs import Construct

class LambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Create the weather function
        self.weather_function = self._create_weather_lambda()
        
        # Now you can access the function ARN
        self.weather_function_arn = self.weather_function.function_arn
      
    def _create_weather_lambda(self):
        fn = lambda_.Function(self, "WeatherFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset("lambda_functions/"),
            handler="weather.handler",
            timeout=Duration.seconds(60),
        )
        
        fn.add_permission("BedrockInvoke",
            principal=iam.ServicePrincipal("bedrock.amazonaws.com"),
            action="lambda:InvokeFunction"
        )
        
        return fn