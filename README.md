# Bedrock_Simple_Agent
A CDK for setting up an Agent + KB + Action

# Setup RAG Stack with CDK

## Prerequisites

- AWS Account with appropriate permissions to provision Bedrock agents.
- Python 3.11 (that's what i used at time of creation...)
- AWS CLI
- CDK CLI

## Step 1: Clone the repositry
```
git clone https://github.com/adija1/Bedrock_Simple_Agent
cd Bedrock_Simple_Agent
```

## Step 2: Configure AWS CLI

Run the following command and enter your AWS credentials (Ensure that the credentials used have the necessary permissions to create and manage Bedrock
agents)

```
aws configure
```

## Step 3: Install CDK if you haven't done so already

```
npm install -g aws-cdk
```

## Step 4: Install dependencies

```
pip install -r requirements.txt
```

## Step 5: Setup environment variables

```
export ACCOUNT_ID=<your-account-id>
export ACCOUNT_REGION=<your-region>
export RAG_PROJ_NAME=<your-project-name>
```

## Step 6: Bootstrap & synth the stack

```
cdk bootstrap
cdk synth
```


## Step 7: Deploy the stack

```
cdk deploy S3Stack
cdk deploy KbRoleStack
cdk deploy OpenSearchServerlessInfraStack
cdk deploy LambdaStack
cdk deploy KbInfraStack
```
## Once the script runs successfully, navigate to the AWS Console:
## Step 8: Sync the Knowledgebase


![image](https://github.com/user-attachments/assets/77ab158b-086e-4d1b-a9cb-af82723b7a9e)


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
