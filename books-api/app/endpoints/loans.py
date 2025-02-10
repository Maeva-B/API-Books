from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.database import loans_collection
from app.schemas import Loan, LoanCreate

router = APIRouter()

