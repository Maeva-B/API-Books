from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.database import loans_collection
from app.schemas import Loan, LoanCreate
from datetime import date
from typing import List, Optional

router = APIRouter()

@router.get("/{loan_id}", response_model=Loan)
async def get_loan(loan_id: str):
    """
    Retrieves a specific loan based on its MongoDB identifier.
    Example URL: GET http://localhost/loans/67a9d43c635513c2db4d7949
    """
    try:
        oid = ObjectId(loan_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid loan ID format")
    
    loan = await loans_collection.find_one({"_id": oid})
    if loan:
        loan["id"] = str(loan["_id"])
        return loan
    raise HTTPException(status_code=404, detail="Loan not found")

@router.get("/", response_model=List[Loan])
async def get_loans(
    loanDate: Optional[str] = None,
    returnDate: Optional[str] = None,
    book_id: Optional[str] = None,
    adherent_id: Optional[str]= None,
    skip: int = 0,
    limit: int = 10
):
    """
    Retrieves all loans with optional filtering by loan date, return date, book id and adherent id, with pagination.

    Example URL:
      GET http://localhost/loans?loanDate=2024-10-06&returnDate=2024-12-30&skip=0&limit=10
      
    Skip (default 0): Indicates the number of loans to skip from the beginning of the result set.
    
    Limit (default 10): Indicates the maximum number of loans to return.
    """
    query = {}
    if loanDate:
        query["loanDate"] = loanDate
    if returnDate:
        query["returnDate"] = returnDate
    if book_id:
        query["book_id"] = book_id
    if adherent_id:
        query["adherent_id"] = adherent_id
    print(query)
    loans_cursor = loans_collection.find(query).skip(skip).limit(limit)
    loans = await loans_cursor.to_list(length=limit)
    for loan in loans:
        # Convert the MongoDB ObjectId to string and assign it to 'id'
        loan["id"] = str(loan["_id"])
    if loans:
        return loans
    raise HTTPException(status_code=404, detail="No loans found")

@router.post("/", response_model=Loan, status_code=status.HTTP_201_CREATED)
async def create_loan(loan : LoanCreate):
    """
    Creates a new loan.

    Example URL:
      POST http://localhost/loans

    Example payload:
      {
          "loanDate": "2025-04-20",
          "returnDate": "2025-04-27",
          "book_id": "2",
          "adherent_id": "0"
      }
    """
    
    loan_doc = loan.dict()
    loan_doc['loanDate'] = loan_doc['loanDate'].isoformat()
    loan_doc['returnDate'] = loan_doc['returnDate'].isoformat()
    result = await loans_collection.insert_one(loan_doc)
    # Append the generated id to the document.
    loan_doc["id"] = str(result.inserted_id)
    return loan_doc