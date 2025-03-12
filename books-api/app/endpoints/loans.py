import re
from typing import List, Optional

from app.database import loans_collection
from app.schemas import Loan, LoanCreate
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

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
        loan["book_id"] = str(loan["book_id"])
        loan["adherent_id"] = str(loan["adherent_id"])
        return loan
    raise HTTPException(status_code=404, detail="Loan not found")


@router.get("/", response_model=List[Loan])
async def get_loans(
    loanDate: Optional[str] = None,
    returnDate: Optional[str] = None,
    book_id: Optional[str] = None,
    adherent_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
):
    """
    Retrieves all loans with optional filtering.
    """
    query = {}
    if loanDate:
        query["loanDate"] = loanDate
    if returnDate:
        query["returnDate"] = returnDate

    if book_id:
        try:
            query["book_id"] = ObjectId(book_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid book_id format")

    if adherent_id:
        try:
            query["adherent_id"] = ObjectId(adherent_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid adherent_id format")

    loans_cursor = loans_collection.find(query).skip(skip).limit(limit)
    loans = await loans_cursor.to_list(length=limit)
    for loan in loans:
        loan["id"] = str(loan["_id"])
        loan["book_id"] = str(loan["book_id"])
        loan["adherent_id"] = str(loan["adherent_id"])
    if loans:
        return loans
    raise HTTPException(status_code=404, detail="No loans found")


@router.post("/", response_model=Loan, status_code=status.HTTP_201_CREATED)
async def create_loan(loan: LoanCreate):
    """
    Creates a new loan.
    """
    try:
        loan_doc = loan.dict()
        loan_doc["loanDate"] = loan_doc["loanDate"].isoformat()
        loan_doc["returnDate"] = (
            loan_doc["returnDate"].isoformat() if loan_doc["returnDate"] else None
        )

        loan_doc["book_id"] = ObjectId(loan.book_id)
        loan_doc["adherent_id"] = ObjectId(loan.adherent_id)

        result = await loans_collection.insert_one(loan_doc)
        loan_doc["_id"] = str(result.inserted_id)
        loan_doc["book_id"] = str(loan_doc["book_id"])
        loan_doc["adherent_id"] = str(loan_doc["adherent_id"])

        return loan_doc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{loan_id}", response_model=Loan, status_code=status.HTTP_200_OK)
async def update_loan(loan_id: str, loan: LoanCreate):
    """
    Updates an existing loan.
    """
    try:
        oid = ObjectId(loan_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid loan ID format"
        )

    loan_doc = loan.dict()
    loan_doc["loanDate"] = loan_doc["loanDate"].isoformat()
    loan_doc["returnDate"] = loan_doc["returnDate"].isoformat()
    update_result = await loans_collection.update_one({"_id": oid}, {"$set": loan_doc})

    if update_result.modified_count == 1:
        updated_loan = await loans_collection.find_one({"_id": oid})
        if updated_loan:
            updated_loan["id"] = str(updated_loan["_id"])
            updated_loan["book_id"] = str(updated_loan["book_id"])
            updated_loan["adherent_id"] = str(updated_loan["adherent_id"])
            return updated_loan

    existing_loan = await loans_collection.find_one({"_id": oid})
    if not existing_loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found"
        )

    existing_loan["id"] = str(existing_loan["_id"])
    existing_loan["book_id"] = str(existing_loan["book_id"])
    existing_loan["adherent_id"] = str(existing_loan["adherent_id"])
    return existing_loan


@router.delete("/{loan_id}", status_code=status.HTTP_200_OK)
async def delete_loan(loan_id: str):
    """
    Deletes an existing loan.
    """
    try:
        oid = ObjectId(loan_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid loan ID format"
        )

    result = await loans_collection.delete_one({"_id": oid})
    if result.deleted_count == 1:
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")


@router.delete("/", response_model=int, status_code=status.HTTP_200_OK)
async def delete_all_loan(
    loanDate: Optional[str] = None,
    returnDate: Optional[str] = None,
    book_id: Optional[str] = None,
    adherent_id: Optional[str] = None,
):
    """
    Deletes all loans matching the provided filters.
    Returns the number of deleted loans.
    """
    query = {}
    if loanDate:
        if re.match("^[0-9]{4}-[0-1][0-9]-[0-9]{2}$", f"{loanDate}"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid loan date format",
            )
        query["loanDate"] = loanDate

    if returnDate:
        if re.match("^[0-9]{4}-[0-1][0-9]-[0-9]{2}$", f"{returnDate}"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid return date format",
            )
        query["returnDate"] = returnDate

    if book_id:
        try:
            query["book_id"] = ObjectId(book_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid book_id format")

    if adherent_id:
        try:
            query["adherent_id"] = ObjectId(adherent_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid adherent_id format")

    result = await loans_collection.delete_many(query)
    if result.deleted_count >= 1:
        return result.deleted_count
    return 0
