import os
import asyncio
import json
from cosmos.cosmos_apis import Cosmos
from dotenv import load_dotenv

load_dotenv()

cosmos: Cosmos = Cosmos() # get instance of cosmos to be able to mmake db calls for chat history

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()

async def create_thread(messages):
    response = await cosmos.create_thread(messages)
    return response

async def update_thread(messages):
    response = await cosmos.update_thread(messages)
    return response

async def get_threads(user):
    response = await cosmos.get_threads(user)
    return response

async def get_thread_by_id(id):
    response = await cosmos.get_thread_by_id(id)
    return response

async def delete_thread(id):
    response = await cosmos.delete_thread(id)
    return response

async def rename_thread(id, newTitle):
    response = await cosmos.rename_thread(id, newTitle)
    return response


if __name__ == '__main__':
    
    c = open_file("./json/create.json")
    json_c = json.loads(c)


    r = asyncio.run(rename_thread("thread_j0mAqiaHc4KyrRGqbX4ejxNE", "This is the new title"))
    #r = asyncio.run(get_thread_by_id("cdadd740-03a9-4ec6-96d0-047099f76988"))
    #r_json = json.loads(r)

    print(r)
