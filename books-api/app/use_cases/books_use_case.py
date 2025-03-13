from app.repositories import books_repository
from app.schemas import BookCreate, TypeEnum


async def get_book_use_case(book_id: str) -> dict:
    book = await books_repository.find_by_id(book_id)
    if book:
        book["id"] = str(book["_id"])
        # Convertir l'ID de l'auteur en chaîne si nécessaire
        if "author_id" in book:
            book["author_id"] = str(book["author_id"])
    return book


async def list_books_use_case(
    title: str = None, 
    description: str = None,
    location: str = None,
    label: str = None,
    type: TypeEnum = None,
    publishDate: str = None,
    publisher: str = None,
    language: str = None,
    link: str = None,
    author_id: str = None,
    skip: int = 0,
    limit: int = 10
) -> list:
    query = {}
    query = {}
    if title:
        query["title"] = {"$regex": rf"{title}", "$options": "i"}
    if description:
        query["description"] = {"$regex": rf"{description}", "$options": "i"}
    if location:
        query["location"] = {"$regex": rf"{location}", "$options": "i"}
    if label:
        query["label"] = {"$regex": rf"{label}", "$options": "i"}
    if type:
        query["type"] = type
    if publishDate:
        query["publishDate"] = publishDate
    if publisher:
        query["publisher"] = {"$regex": rf"{publisher}", "$options": "i"}
    if language:
        query["language"] = {"$regex": rf"{language}", "$options": "i"}
    if link:
        query["link"] = {"$regex": rf"{link}", "$options": "i"}
    if author_id:
        query["author_id"] = author_id
    
    books = await books_repository.find_all(query, skip, limit)
    for book in books:
        book["id"] = str(book["_id"])
        if "author_id" in book:
            book["author_id"] = str(book["author_id"])
    return books


async def create_book_use_case(book_data: BookCreate) -> dict:
    book_doc = book_data.dict()
    # Convert the publication date into ISO string
    book_doc["publishDate"] = book_doc["publishDate"].isoformat()
    inserted_id = await books_repository.insert_book(book_doc)
    book_doc["id"] = inserted_id
    return book_doc


async def update_book_use_case(book_id: str, book_data: BookCreate) -> dict:
    book_doc = book_data.dict()
    # Convert the publication date into ISO string
    book_doc["publishDate"] = book_doc["publishDate"].isoformat()
    modified_count = await books_repository.update_book(book_id, book_doc)
    if modified_count == 1:
        updated_book = await books_repository.find_by_id(book_id)
        if updated_book:
            updated_book["id"] = str(updated_book["_id"])
            if "author_id" in updated_book:
                updated_book["author_id"] = str(updated_book["author_id"])
            return updated_book
    existing_book = await books_repository.find_by_id(book_id)
    if existing_book:
        existing_book["id"] = str(existing_book["_id"])
        if "author_id" in existing_book:
            existing_book["author_id"] = str(existing_book["author_id"])
        return existing_book
    return None


async def delete_book_use_case(book_id: str) -> bool:
    deleted_count = await books_repository.delete_book(book_id)
    return deleted_count == 1


async def get_author_by_book_use_case(book_id: str) -> list:
    books = await books_repository.find_author_by_book(book_id)
    return books
