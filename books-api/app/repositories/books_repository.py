from app.database import authors_collection, books_collection
from bson import ObjectId


async def find_by_id(book_id: str) -> dict:
    try:
        oid = ObjectId(book_id)
    except Exception:
        return None
    return await books_collection.find_one({"_id": oid})


async def find_all(query: dict, skip: int, limit: int) -> list:
    cursor = books_collection.find(query).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


async def insert_book(book_doc: dict) -> str:
    result = await books_collection.insert_one(book_doc)
    return str(result.inserted_id)


async def update_book(book_id: str, book_doc: dict) -> int:
    try:
        oid = ObjectId(book_id)
    except Exception:
        return 0
    result = await books_collection.update_one({"_id": oid}, {"$set": book_doc})
    return result.modified_count


async def delete_book(book_id: str) -> int:
    try:
        oid = ObjectId(book_id)
    except Exception:
        return 0
    result = await books_collection.delete_one({"_id": oid})
    return result.deleted_count


async def find_author_by_book(book_id: str) -> list:
    try:
        oid = ObjectId(book_id)
    except Exception:
        return []
    book = books_collection.find_one({"_id": oid})
    if not book:
        return {}
    try:
        author_id = ObjectId(book["author_id"])
    except Exception:
        return []
    author = authors_collection.find_one({"_id": author_id})
    author["_id"] = str(author["_id"])
    return author
