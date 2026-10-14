import os

from pymongo import MongoClient


MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://localhost:27017",
)

DATABASE_NAME = os.getenv(
    "MONGODB_DATABASE",
    "employee_db",
)

COLLECTION_NAME = os.getenv(
    "MONGODB_COLLECTION",
    "employees",
)


client = MongoClient(MONGODB_URI)

database = client[DATABASE_NAME]

employees_collection = database[COLLECTION_NAME]