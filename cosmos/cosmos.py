import os
import json
import azure.cosmos.cosmos_client as cosmos_client
from dotenv import load_dotenv

load_dotenv()

class Cosmos:
    
    def __init__(self):
        HOST = os.environ.get("HOST")
        MASTER_KEY = os.environ.get("MASTER_KEY")

        self.cosmos_client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="ShadowSellerCosmosAgent", user_agent_overwrite=True)

    async def get_conversation_history(self):
        DATABASE_ID = os.environ.get("DATABASE_ID")
        CONTAINER_ID = os.environ.get("CONTAINER_ID")

        db = self.cosmos_client.get_database_client(DATABASE_ID)
        #print('Database with id \'{0}\' was found'.format(DATABASE_ID))
        container = db.get_container_client(CONTAINER_ID)
        #print('Container with id \'{0}\' was found'.format(CONTAINER_ID))
        
        items = list(container.query_items(
            query="SELECT * FROM r WHERE r.user=@user",
            parameters=[
                { "name":"@user", "value": "joelborellis@outlook.com" }
            ],
            enable_cross_partition_query=True,
        ))

        return (json.dumps(items))
    
    async def get_single_conversation(self, id):
        DATABASE_ID = os.environ.get("DATABASE_ID")
        CONTAINER_ID = os.environ.get("CONTAINER_ID")

        db = self.cosmos_client.get_database_client(DATABASE_ID)
        #print('Database with id \'{0}\' was found'.format(DATABASE_ID))
        container = db.get_container_client(CONTAINER_ID)
        #print('Container with id \'{0}\' was found'.format(CONTAINER_ID))
        
        items = list(container.query_items(
            query="SELECT * FROM r WHERE r.id=@id",
            parameters=[
                { "name":"@id", "value": id }
            ],
            enable_cross_partition_query=True,
        ))

        return (json.dumps(items))