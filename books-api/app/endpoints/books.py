from typing import List, Optional

from app.database import books_collection
from app.schemas import Book, BookCreate, TypeEnum
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str):
    """
    Retrieves a specific book based on its MongoDB identifier.
    Example URL: GET http://localhost/books/67a36d9a198cd394f628c25c
    """
    try:
        oid = ObjectId(book_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    book = await books_collection.find_one({"_id": oid})
    if book:
        book["id"] = str(book["_id"])
        # Convertir l'ID de l'auteur en chaîne si nécessaire
        if "author_id" in book:
            book["author_id"] = str(book["author_id"])
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.get("/", response_model=List[Book])
async def get_books(
    title: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    label: Optional[str] = None,
    type: Optional[TypeEnum] = None,
    publishDate: Optional[str] = None,
    publisher: Optional[str] = None,
    language: Optional[str] = None,
    link: Optional[str] = None,
    author_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
):
    """
    Retrieves all books with optional filtering.
    """
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

    books_cursor = books_collection.find(query).skip(skip).limit(limit)
    books = await books_cursor.to_list(length=limit)
    for book in books:
        book["id"] = str(book["_id"])
        if "author_id" in book:
            book["author_id"] = str(book["author_id"])
    if books:
        return books
    raise HTTPException(status_code=404, detail="No books found")


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    """
    Creates a new book.
    """
    book_doc = book.dict()
    # Convertir la date en chaîne ISO
    book_doc["publishDate"] = book_doc["publishDate"].isoformat()
    result = await books_collection.insert_one(book_doc)
    book_doc["id"] = str(result.inserted_id)
    return book_doc


@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: str, book_data: BookCreate):
    """
    Updates an existing book.
    """
    try:
        oid = ObjectId(book_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book ID format"
        )

    book_doc = book_data.dict()
    book_doc["publishDate"] = book_doc["publishDate"].isoformat()
    update_result = await books_collection.update_one({"_id": oid}, {"$set": book_doc})

    if update_result.modified_count == 1:
        updated_book = await books_collection.find_one({"_id": oid})
        if updated_book:
            updated_book["id"] = str(updated_book["_id"])
            if "author_id" in updated_book:
                updated_book["author_id"] = str(updated_book["author_id"])
            return updated_book

    existing_book = await books_collection.find_one({"_id": oid})
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    existing_book["id"] = str(existing_book["_id"])
    if "author_id" in existing_book:
        existing_book["author_id"] = str(existing_book["author_id"])
    return existing_book


@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: str):
    """
    Deletes an existing book.
    """
    try:
        oid = ObjectId(book_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book ID format"
        )

    result = await books_collection.delete_one({"_id": oid})
    if result.deleted_count == 1:
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
