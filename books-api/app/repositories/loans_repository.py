from app.database import loans_collection
from bson import ObjectId

async def find_by_id(loan_id: str) -> dict:
    try:
        oid = ObjectId(loan_id)
    except Exception:
        return None
    return await loans_collection.find_one({"_id": oid})


async def find_all(query: dict, skip: int, limit: int) -> list:
    cursor = loans_collection.find(query).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


async def insert_loan(loan_doc: dict) -> str:
    result = await loans_collection.insert_one(loan_doc)
    return str(result.inserted_id)


async def update_loan(loan_id: str, loan_doc: dict) -> int:
    try:
        oid = ObjectId(loan_id)
    except Exception:
        return 0
    result = await loans_collection.update_one({"_id": oid}, {"$set": loan_doc})
    return result.modified_count


async def delete_loan(loan_id: str) -> int:
    try:
        oid = ObjectId(loan_id)
    except Exception:
        return 0
    result = await loans_collection.delete_one({"_id": oid})
    return result.deleted_count

async def delete_all_loan(
        query: dict,
        ) -> int:
    
    result = await loans_collection.delete_many(query)
    return result.deleted_count
