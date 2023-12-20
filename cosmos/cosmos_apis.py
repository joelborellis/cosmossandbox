import os
import json
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from dotenv import load_dotenv

load_dotenv()

class Cosmos:
    
    def __init__(self):
        HOST = os.environ.get("HOST")
        MASTER_KEY = os.environ.get("MASTER_KEY")
        DATABASE_ID = os.environ.get("DATABASE_ID")
        CONTAINER_ID = os.environ.get("CONTAINER_ID")

        self.cosmos_client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="ShadowSellerCosmosAgent", user_agent_overwrite=True)
        self.db = self.cosmos_client.get_database_client(DATABASE_ID)
        self.container = self.db.get_container_client(CONTAINER_ID)

    async def upsert_thread(self, options: dict):
        try:
            response = self.container.upsert_item(options)
        except exceptions as e:
            return ('ERROR: cosmos.upsert_item - Resource already exists'.format(e))
        
        return ('cosmos.upsert_thread - Created item\'s Id is {0}'.format(response['id']))

    
    async def get_threads(self, user: str):
        try:
            items = list(self.container.query_items(
                query="SELECT r.id, r.title, r.user, r.messages, TimestampToDateTime(r._ts*1000) AS 'time' FROM Convos r WHERE r.user=@user",
                parameters=[
                    { "name":"@user", "value": user }
                ],
                enable_cross_partition_query=True,
            ))
        except exceptions.CosmosResourceNotFoundError as e:
            return ('ERROR: cosmos.get_threads - Cannot find threads')

        return ('cosmos.get_threads - Retrieved total items'.format(items.count))
    
    async def get_thread_by_id(self, id: str):
        try:
            items = list(self.container.query_items(
                query="SELECT r.id, r.title, r.user, r.messages, TimestampToDateTime(r._ts*1000) AS 'time' FROM Convos r WHERE r.id=@id",
                parameters=[
                    { "name":"@id", "value": id }
                ],
                enable_cross_partition_query=True,
            ))
        except exceptions.CosmosResourceNotFoundError as e:
            return ('ERROR: cosmos.get_thread_by_id - Cannot find thread')
    
        return ('cosmos.get_thread_by_id - Retrieved item Id is {0}'.format(items[0].get("id")))
    
    async def delete_thread(self, id: str):
        try:
            self.container.delete_item(item=id,partition_key=id)
        except exceptions.CosmosResourceNotFoundError  as e:
            return ('ERROR: cosmos.delete_thread - Resource does not exist')
        
        return ('cosmos.delete_thread - Deleted item\'s Id is {0}'.format(id))
    
    async def rename_thread(self, id: str, newTitle: str):
        try:

            item = self.container.read_item(id, partition_key=id)
            item["title"] = newTitle
            updated_item = self.container.upsert_item(item)

        except exceptions.CosmosResourceNotFoundError  as e:
            return ('ERROR: cosmos.rename_thread - Resource does not exist')
        
        return ('cosmos.rename_thread - Renamed items Id is {0}'.format(id))