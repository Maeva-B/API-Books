from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.database import books_collection
from app.schemas import Book, BookCreate, TypeEnum
from typing import List, Optional

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
    print("coucou")
    book = await books_collection.find_one({"_id": oid})
    print("coucou2")
    if book:
        book["id"] = str(book["_id"])
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.get("/", response_model=List[Book])
async def get_books(
    title: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    label: Optional[str]= None,
    type: Optional[TypeEnum] = None,
    publishDate: Optional[str] = None,
    publisher: Optional[str] = None,
    language: Optional[str] = None,
    link: Optional[str] = None,
    author_id:Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    """
    Retrieves all books with optional filtering by title, description, location, label, type, publishDate, publisher and language, with pagination.

    Example URL:
      GET http://localhost/loans?title=Network&description=study&location=H2&label=network&type=network&publishDate=2021-09-05&publisher=Kauf&language=ish&link=example&skip=0&limit=10

    Skip (default 0): Indicates the number of loans to skip from the beginning of the result set.
    
    Limit (default 10): Indicates the maximum number of loans to return.
    """
    query = {}
    if title:
        query["title"] = { "$regex": rf"{title}", "$options": "i" }
    if description:
        query["description"] = { "$regex": rf"{description}", "$options": "i" }
    if location:
        query["location"] = { "$regex": rf"{location}", "$options": "i" }
    if label:
        query["label"] =  { "$regex": rf"{label}", "$options": "i" }
    if type:
        query["type"] =  type
    if publishDate:
        query["publishDate"] =  publishDate
    if publisher:
        query["publisher"] =  { "$regex": rf"{publisher}", "$options": "i" }
    if language:
        query["language"] =  { "$regex": rf"{language}", "$options": "i" }
    if link:
        query["link"] =  { "$regex": rf"{link}", "$options": "i" }
    if author_id:
        query["author_id"] =  author_id
    
    print(query)
    books_cursor = books_collection.find(query).skip(skip).limit(limit)
    books = await books_cursor.to_list(length=limit)
    for book in books:
        # Convert the MongoDB ObjectId to string and assign it to 'id'
        book["id"] = str(book["_id"])
    if books:
        return books
    raise HTTPException(status_code=404, detail="No books found")

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book : BookCreate):
    """
    Creates a new book.

    Example URL:
      POST http://localhost/books

    Example payload:
      {
        "title": "Advanced Quantum Mechanics",
        "description": "An in-depth exploration of quantum mechanics and its modern applications.",
        "location": "Shelf M7",
        "label": "Quantum Physics",
        "type": "physic",
        "publishDate": "2024-02-10",
        "publisher": "Harvard University Press",
        "language": "English",
        "link": "https://example.com/advanced-quantum-mechanics",
        "author_id":"3"
        }

    """
    
    book_doc = book.dict()
    book_doc['publishDate'] = book_doc['publishDate'].isoformat()
    result = await books_collection.insert_one(book_doc)
    # Append the generated id to the document.
    book_doc["id"] = str(result.inserted_id)
    return book_doc

@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: str, loan: BookCreate):
    """
    Updates an existing book

    Example URL: PUT http://localhost/books/67a391a4198cd394f628c25f

    Example payload:
    {
        "title": "Advanced Quantum Mechanics",
        "description": "An in-depth exploration of quantum mechanics and its modern applications.",
        "location": "Shelf M7",
        "label": "Quantum Physics",
        "type": "physic",
        "publishDate": "2024-02-10",
        "publisher": "Harvard University Press",
        "language": "English",
        "link": "https://example.com/advanced-quantum-mechanics",
        "author_id":"3"
    }
    """
    # Retrieve the book id
    try:
        oid = ObjectId(book_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book ID format")

    book_doc = loan.dict()
    book_doc['publishDate'] = book_doc['publishDate'].isoformat()
    update_result = await books_collection.update_one({"_id": oid}, {"$set": book_doc})

    if update_result.modified_count == 1:
        updated_book = await books_collection.find_one({"_id": oid})
        if updated_book:
            updated_book["id"] = str(updated_book["_id"])
            return updated_book

    # Check if the loan exists; if not, raise a 404 error.
    existing_book = await books_collection.find_one({"_id": oid})
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    # If no modifications were made, return the existing loan.
    existing_book["id"] = str(existing_book["_id"])
    return existing_book

@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: str):
    """
    Deletes an existing book.
    Example URL: DELETE http://localhost/books/67a391a4198cd394f628c25f
    """
    try:
        oid = ObjectId(book_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book ID format")

    result = await books_collection.delete_one({"_id": oid})
    if result.deleted_count == 1:
        return  # HTTP 204 No Content
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Book not found")
