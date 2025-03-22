import os

EMBEDDING_MODEL_IDs = ["amazon.titan-embed-text-v2:0"]
CHUNKING_STRATEGIES = {0:"Default chunking",1:"Fixed-size chunking", 2:"No chunking"}

class EnvSettings:
    # General params
    ACCOUNT_ID =  os.getenv("ACCOUNT_ID", "123456789012") 
    ACCOUNT_REGION = os.getenv("ACCOUNT_REGION", "us-east-1")
    RAG_PROJ_NAME = os.getenv("RAG_PROJ_NAME", "kb-stack") 
    
class KbConfig:
    KB_ROLE_NAME = f"{EnvSettings.RAG_PROJ_NAME}-kb-role"
    EMBEDDING_MODEL_ID = EMBEDDING_MODEL_IDs[0]
    CHUNKING_STRATEGY = CHUNKING_STRATEGIES[0] # TODO: Choose the Chunking option 0,1,2
    MAX_TOKENS = 512 # TODO: Change this value accordingly if you choose "FIXED_SIZE" chunk strategy
    OVERLAP_PERCENTAGE = 20 # TODO: Change this value accordingly
    
    # Agent Config
    AGENT_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
    AGENT_INSTRUCTION = "You are a helpful assistant that uses the knowledge base for general questions and the weather action group for weather-related queries. Always check if the user is asking about weather before using the action group."

class OpenSearchServerlessConfig:
    COLLECTION_NAME = f"{EnvSettings.RAG_PROJ_NAME}-kb-collection"
    INDEX_NAME = f"{EnvSettings.RAG_PROJ_NAME}-kb-index"