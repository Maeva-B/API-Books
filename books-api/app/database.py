"""Module that provide the database connection."""

import motor.motor_asyncio

# Connection details
MONGO_DETAILS = "mongodb://localhost:27017"

# Creating an asynchronous client for MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.books_api

books_collection = database.get_collection("books")
authors_collection = database.get_collection("authors")
adherents_collection = database.get_collection("adherents")
