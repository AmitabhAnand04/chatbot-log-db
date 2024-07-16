import os
import datetime
from azure.cosmos import CosmosClient, exceptions
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the Cosmos client using environment variables
url = os.getenv("COSMOS_DB_ACCOUNT_URL")
key = os.getenv("COSMOS_DB_ACCOUNT_KEY")
client = CosmosClient(url, key)

# Define the database and container
database_name = 'chatbot_log_db'
container_name = 'ConversationError'

database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

def conversation_error(convId, user, userName, sessionId, convPrompt, convIntent, errorMessage):
    try:
        # Create the document
        error_log = {
            'id': convId,  # Unique identifier for the document
            'user': user,
            'userName': userName,
            'sessionId': sessionId,
            'convPrompt': convPrompt,
            'convIntent': convIntent,
            'errorMessage': errorMessage,
            'errorDateTime': datetime.datetime.now().isoformat()
        }
        
        # Create the item in the container
        container.create_item(body=error_log)
        return "Success"
        
    except exceptions.CosmosResourceExistsError:
        return "Failure: An error log with the same ID already exists."
    except exceptions.CosmosHttpResponseError as e:
        return f"Failure: An error occurred - {e.message}"

# Example usage
status = conversation_error(
    convId='error_12345',
    user='12345',
    userName='Amitabh Anand',
    sessionId='session_12345',
    convPrompt='How do I integrate Cosmos DB with Python?',
    convIntent='IntegrationQuestion',
    errorMessage='Timeout error while accessing Cosmos DB.'
)

print(status)
