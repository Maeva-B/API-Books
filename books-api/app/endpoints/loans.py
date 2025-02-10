from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.database import loans_collection
from app.schemas import Loan, LoanCreate

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
