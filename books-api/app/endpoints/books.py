from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.database import books_collection
from app.schemas import Book, BookCreate

router = APIRouter()

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str):
    """
    Retrieves a specific book based on its MongoDB identifier.
    Example URL: GET http://localhost/book/67a36d9a198cd394f628c25c
    """
    try:
        oid = ObjectId(book_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    
    book = await books_collection.find_one({"_id": oid})
    if book:
        book["id"] = str(book["_id"])
        return book
    raise HTTPException(status_code=404, detail="Book not found")
