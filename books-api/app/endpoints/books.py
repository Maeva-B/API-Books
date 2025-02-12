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
      GET http://localhost/loans?loanDate=2024-10-06&returnDate=2024-12-30&skip=0&limit=10
      
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

# @router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
# async def create_loan(loan : LoanCreate):
#     """
#     Creates a new loan.

#     Example URL:
#       POST http://localhost/loans

#     Example payload:
#       {
#           "loanDate": "2025-04-20",
#           "returnDate": "2025-04-27",
#           "book_id": "2",
#           "adherent_id": "0"
#       }
#     """
    
#     loan_doc = loan.dict()
#     loan_doc['loanDate'] = loan_doc['loanDate'].isoformat()
#     loan_doc['returnDate'] = loan_doc['returnDate'].isoformat()
#     result = await loans_collection.insert_one(loan_doc)
#     # Append the generated id to the document.
#     loan_doc["id"] = str(result.inserted_id)
#     return loan_doc

# @router.put("/{loan_id}", response_model=Loan, status_code=status.HTTP_200_OK)
# async def update_loan(loan_id: str, loan: LoanCreate):
#     """
#     Updates an existing loan

#     Example URL: PUT http://localhost/loans/67a391a4198cd394f628c25f

#     Example payload:
#     {
#         "loanDate": "2025-04-20",
#         "returnDate": "2025-04-27",
#         "book_id": "2",
#         "adherent_id": "0"
#     }
#     """
#     # Retrieve the loan id
#     try:
#         oid = ObjectId(loan_id)
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid loan ID format")

#     loan_doc = loan.dict()
#     loan_doc['loanDate'] = loan_doc['loanDate'].isoformat()
#     loan_doc['returnDate'] = loan_doc['returnDate'].isoformat()
#     update_result = await loans_collection.update_one({"_id": oid}, {"$set": loan_doc})

#     if update_result.modified_count == 1:
#         updated_loan = await loans_collection.find_one({"_id": oid})
#         if updated_loan:
#             updated_loan["id"] = str(updated_loan["_id"])
#             return updated_loan

#     # Check if the loan exists; if not, raise a 404 error.
#     existing_loan = await loans_collection.find_one({"_id": oid})
#     if not existing_loan:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")

#     # If no modifications were made, return the existing loan.
#     existing_loan["id"] = str(existing_loan["_id"])
#     return existing_loan

# @router.delete("/{loan_id}", status_code=status.HTTP_200_OK)
# async def delete_loan(loan_id: str):
#     """
#     Deletes an existing loan.
#     Example URL: DELETE http://localhost/loans/67a391a4198cd394f628c25f
#     """
#     try:
#         oid = ObjectId(loan_id)
#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid loan ID format")

#     result = await loans_collection.delete_one({"_id": oid})
#     if result.deleted_count == 1:
#         return  # HTTP 204 No Content
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail="Loan not found")
