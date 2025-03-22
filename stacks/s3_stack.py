from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy,
    Stack,
)
from constructs import Construct

class S3Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket to store travel insurance PDFs
        self.bucket = s3.Bucket(
            self, "KnowledgeBaseBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

    @property
    def bucket_name(self) -> str:
        return self.bucket.bucket_name