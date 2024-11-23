"""
MOVING THE MONGODB SERVER ON PREMISES TO ATLAS
"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import os
from dotenv import load_dotenv


load_dotenv()

uri = f"mongodb+srv://{os.getenv('ATLAS_USER_NAME')}:{os.getenv('ATLAS_PASSWORD')}@mycluster.fcceezx.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Open the JSON file
with open('database_backups/MongoDB/canonical_extended_shootings_json.CBM_18_06_2024_2000.json') as f:
    data = json.load(f)

len(data)
# Get a reference to the database and collection you want to import into
db = client['CBM']
collection = db['shootings']


for d in range(len(data)):
    try:
        data[d]['_id'] = data[d]['_id']['$oid']
        result=collection.insert_one(data[d])
    except Exception as e:
        print(e) 
        

