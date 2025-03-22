import json
import random

def handler(event, context):
    print("event ", event)
    
    api_path = event["apiPath"]
    city = event["parameters"][0]["value"]
    temperature = random.randint(10, 40)
    
    response_json = {"temperature": str(temperature)}
    response_body = {
        "application/json": {
            "body": json.dumps(response_json)
        }
    }
    
    # Construct the action response
    action_response = {
        "actionGroup": event["actionGroup"],
        "apiPath": event["apiPath"],
        "httpMethod": event["httpMethod"],
        "parameters": event["parameters"],
        "httpStatusCode": 200,
        "responseBody": response_body,
    }

    # Preserve session attributes
    session_attributes = event.get("sessionAttributes", {})
    prompt_session_attributes = event.get("promptSessionAttributes", {})

    return {
        "messageVersion": "1.0",
        "response": action_response,
        "sessionAttributes": session_attributes,
        "promptSessionAttributes": prompt_session_attributes,
    }
