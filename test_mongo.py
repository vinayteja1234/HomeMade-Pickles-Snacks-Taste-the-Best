import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.environ.get('MONGO_URI')
print(f"Connecting to: {mongo_uri}")

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("Successfully connected to MongoDB Atlas!")
    
    db = client['pickledb']
    count = db['users'].count_documents({})
    print(f"Number of users in pickledb: {count}")
    
except Exception as e:
    print(f"Connection failed: {e}")
