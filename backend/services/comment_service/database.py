from pymongo import MongoClient

import os
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["helpdesk"]

users_col = db["users"]
tickets_col = db["tickets"]
comments_col = db["comments"]   # add this line