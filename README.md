# Bedrock_Simple_Agent
A CDK for setting up an Agent + KB + Action

# Setup RAG Stack with CDK

## Prerequisites

- Python 3.11
- AWS CLI
- CDK CLI

## Setup 

1. Setup AWS CLI

```
aws configure
```

2. Install CDK

```
npm install -g aws-cdk
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Setup environment variables

```
export ACCOUNT_ID=<your-account-id>
export ACCOUNT_REGION=<your-region>
export RAG_PROJ_NAME=<your-project-name>
```

5. Bootstrap the stack

```
cdk bootstrap
```

6. Synthesize the CloudFormation template

```
cdk synth
```

7. Deploy the stack

```
cdk deploy S3Stack
cdk deploy KbRoleStack
cdk deploy OpenSearchServerlessInfraStack
cdk deploy LambdaStack
cdk deploy KbInfraStack
```

8. To Destroy the stack(s)

```
cdk destroy --all 
```

To add additional dependencies, for example other CDK libraries, just add them to your setup.py file and rerun the pip install -r requirements.txt command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
