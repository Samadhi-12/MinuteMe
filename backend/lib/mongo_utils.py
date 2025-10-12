from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB", "minuteme")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def insert_agenda(agenda):
    return db.agendas.insert_one(agenda).inserted_id

def get_latest_agenda():
    return db.agendas.find_one(sort=[("_id", -1)])

# Add more functions as needed