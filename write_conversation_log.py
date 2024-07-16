import datetime
import uuid
from azure.cosmos import CosmosClient, exceptions

# Initialize the Cosmos client
url = "CosmosDB Url"
key = "CosmosDB Key"
client = CosmosClient(url, key)

# Define the database and container
database_name = 'chatbot_log_db'
container_name = 'ConversationLog'

database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

def write_conversation_log(user, userName, sessionId, convDateTime, convPrompt, convIntent,
                           convResponse, convStatus, generatedSQL, generatedSQLResults, otherInfo):
    try:
        # Create the document
        conversation_log = {
            'id': str(uuid.uuid4()), #f"{sessionId}-{user}",  # Unique identifier for the document
            'user': user,
            'userName': userName,
            'sessionId': sessionId,
            'convDateTime': convDateTime.isoformat(),
            'convPrompt': convPrompt,
            'convIntent': convIntent,
            'convResponse': convResponse,
            'convStatus': convStatus,
            'generatedSQL': generatedSQL,
            'generatedSQLResults': generatedSQLResults,
            'otherInfo': otherInfo
        }
        
        # Create the item in the container
        container.create_item(body=conversation_log)
        return "Success"
        
    except exceptions.CosmosResourceExistsError:
        return "Failure: A conversation log with the same ID already exists."
    except exceptions.CosmosHttpResponseError as e:
        return f"Failure: An error occurred - {e.message}"
    
# Example usage
status = write_conversation_log(
    user='12345',
    userName='Amitabh Anand',
    sessionId='session_12345',
    convDateTime=datetime.datetime.now(),
    convPrompt='How do I integrate Cosmos DB with Python?',
    convIntent='IntegrationQuestion',
    convResponse='You can use the azure-cosmos package...',
    convStatus='Success',
    generatedSQL=None,
    generatedSQLResults=None,
    otherInfo='No additional information'
)
print(status)