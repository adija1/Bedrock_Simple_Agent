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

1. Navigate to the S3 and choose the bucket that was provisioned by the stack
![image](https://github.com/user-attachments/assets/77ab158b-086e-4d1b-a9cb-af82723b7a9e)

2. Upload documents for bedrock agent to use as knowledge base, here i using following document for demo: [GreenhouseEffectArchive.pdf](https://www.healthandenvironment.org/docs/ToxipediaGreenhouseEffectArchive.pdf)
3. Navigate to the Bedrock and click on Knowledge Base on the left panel, you should see like this:
![image](https://github.com/user-attachments/assets/42435e3f-1ff4-49f9-b3b6-fc039793c8fe)
4. Click on the Knowledge Bases
5. Tick on the Data Source (s3) and click on sync:
![image](https://github.com/user-attachments/assets/8785bdaf-0371-4ccf-accb-300603211181)

## Step 9: Test Bedrock Agent

1. In Bedrock console click on Agents on the left panel, you should see that your agent is in NOT_PREPARED status.
![image](https://github.com/user-attachments/assets/51a6e7e5-429e-4cee-b861-55328c24eb04)

2. Click on "Edit in Agent Builder" and cross check if everything it’s set up correctly then click on Save and Exit.
![image](https://github.com/user-attachments/assets/2fd191b9-59c8-4908-a230-efc2e8aec8d0)

3. For Testing Agent click on the Prepare button on the right and wait for status become PREPARED
![image](https://github.com/user-attachments/assets/3ecec30c-3576-4917-a3bd-809f283fddba)

4. Test with knowledge base, you can ask anything from the document, for example ask about the greenhouse effect and you will see that the agent will also reference the document:
![image](https://github.com/user-attachments/assets/ee250898-f545-4499-9ba0-57f160ec8127)

5. Test the action group by asking about temperature of a City and see how it uses the Lambda function
![image](https://github.com/user-attachments/assets/92ae2991-7968-4962-baa3-84bc2e3ba585)


## Destroy the stack(s)

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
