from app.database import adherents_collection, loans_collection
from bson import ObjectId


async def find_by_id(adherent_id: str) -> dict:
    try:
        oid = ObjectId(adherent_id)
    except Exception:
        return None
    return await adherents_collection.find_one({"_id": oid})


async def find_all(query: dict, skip: int, limit: int) -> list:
    adherents_cursor = adherents_collection.find(query).skip(skip).limit(limit)
    return await adherents_cursor.to_list(length=limit)


async def insert_adherent(adherent_doc: dict) -> str:
    result = await adherents_collection.insert_one(adherent_doc)
    return str(result.inserted_id)


async def update_adherent(adherent_id: str, adherent_doc: dict) -> int:
    try:
        oid = ObjectId(adherent_id)
    except Exception:
        return 0
    result = await adherents_collection.update_one({"_id": oid}, {"$set": adherent_doc})
    return result.modified_count


async def delete_adherent(adherent_id: str) -> int:
    try:
        oid = ObjectId(adherent_id)
    except Exception:
        return 0
    result = await adherents_collection.delete_one({"_id": oid})
    return result.deleted_count


async def find_by_login(login: str) -> dict:
    return await adherents_collection.find_one({"login": login})


async def find_loans_by_adherent(adherent_id: str) -> list:
    try:
        oid = ObjectId(adherent_id)
    except Exception:
        return []

    cursor = loans_collection.find({"adherent_id": oid})
    loans = await cursor.to_list(length=None)
    return loans
