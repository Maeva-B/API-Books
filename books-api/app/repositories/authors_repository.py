from bson import ObjectId
from app.database import authors_collection

async def find_by_id(author_id: str) -> dict:
    try:
        oid = ObjectId(author_id)
    except Exception:
        return None
    return await authors_collection.find_one({"_id": oid})

async def find_all(query: dict, skip: int, limit: int) -> list:
    cursor = authors_collection.find(query).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)

async def insert_author(author_doc: dict) -> str:
    result = await authors_collection.insert_one(author_doc)
    return str(result.inserted_id)

async def update_author(author_id: str, author_doc: dict) -> int:
    try:
        oid = ObjectId(author_id)
    except Exception:
        return 0
    result = await authors_collection.update_one({"_id": oid}, {"$set": author_doc})
    return result.modified_count

async def delete_author(author_id: str) -> int:
    try:
        oid = ObjectId(author_id)
    except Exception:
        return 0
    result = await authors_collection.delete_one({"_id": oid})
    return result.deleted_count