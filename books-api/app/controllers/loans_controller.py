from typing import List, Optional
import re

from app.schemas import Loan, LoanCreate
from app.use_cases import loans_use_case
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get(
    "/{loan_id}",
    response_model=Loan,
    summary="Retrieve an loan",
)
async def get_loan(loan_id: str):
    """
    Retrieve an loan by its unique identifier.

    - **loan_id**: Unique identifier of the loan.

    **Example Request:**
    ```
    GET /loans/60b725f10c9f1e23d8f3a3e9
    ```
    """
    loan = await loans_use_case.get_loan_use_case(loan_id)
    if loan:
        return loan
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="loan not found"
    )


@router.get(
    "/",
    response_model=List[Loan],
    summary="List loans",
)
async def get_loans(
    loanDate: Optional[str] = None,
    returnDate: Optional[str] = None,
    book_id: Optional[str] = None,
    adherent_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
):
    """
    Retrieve a list of loans.

    - **loanDate**: Filter loans by loan date.
    - **returnDate**: Filter loans by loan deadline.
    - **book_id**: Filter loans by book.
    - **adherent_id**: Filter loans by adherent.
    - **skip**: Number of records to skip.
    - **limit**: Maximum number of records to return.

    **Example Request:**
    ```
    GET /loans?loanDate=2024-12-26&skip=0&limit=10
    ```
    """
    if loanDate and not re.match("^[0-9]{4}-[0-1][0-9]-[0-9]{2}$", f"{loanDate}"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid loan date format",
        )
    if loanDate and not re.match("^[0-9]{4}-[0-1][0-9]-[0-9]{2}$", f"{returnDate}"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid loan date format",
        )
    loans = await loans_use_case.list_loans_use_case(
        loanDate, returnDate, book_id, adherent_id, skip, limit
    )
    if loans:
        return loans
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No loans found"
    )


@router.post(
    "/",
    response_model=Loan,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new loan",
)
async def create_loan(loan: LoanCreate):
    """
    Create a new loan.

    **Request Body:**
    - **loanDate**: loan's date.
    - **returnDate**: loan's return date.
    - **book_id**: borrowed book.
    - **adherent_id**: borrower.

    **Example Request:**
    ```
    POST /loans
    {
      "loanDate": "2025-03-26",
      "returnDate": "2025-04-10",
      "book_id": "67acab929901df1bd44d796b",
      "adherent_id": "67a9d24b635513c2db4d7946"
    }
    ```
    """
    created_loan = await loans_use_case.create_loan_use_case(loan)
    return created_loan


@router.put(
    "/{loan_id}",
    response_model=Loan,
    summary="Update an loan",
)
async def update_loan(loan_id: str, loan: LoanCreate):
    """
    Update an existing loan.

    - **loan_id**: Unique identifier of the loan to update.

    **Example Request:**
    ```
    PUT /loans/60b725f10c9f1e23d8f3a3e9
    {
      "loanDate": "2025-03-26",
      "returnDate": "2025-04-24",
      "book_id": "67acab929901df1bd44d796b",
      "adherent_id": "67a9d24b635513c2db4d7946"
    }
    ```
    """
    updated_loan = await loans_use_case.update_loan_use_case(loan_id, loan)
    if updated_loan:
        return updated_loan
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="loan not found"
    )


@router.delete(
    "/{loan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an loan",
)
async def delete_loan(loan_id: str):
    """
    Delete an loan by its unique identifier.

    **Example Request:**
    ```
    DELETE /loans/60b725f10c9f1e23d8f3a3e9
    ```

    **Response:**
    HTTP 204 No Content
    """
    success = await loans_use_case.delete_loan_use_case(loan_id)
    if success:
        return  # HTTP 204 No Content
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="loan not found"
    )



@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an loan",
)
async def delete_all_loan(
    loanDate: Optional[str] = None,
    returnDate: Optional[str] = None,
    book_id: Optional[str] = None,
    adherent_id: Optional[str] = None,
):
    """
    Deletes all loans matching the provided filters.
    Returns the number of deleted loans.

    **Example Request:**
    ```
    DELETE http://localhost:8000/loans?loanDate=2012-10-10&book_id=0
    ```

    **Response:**
    HTTP 204 No Content
    """
    if not re.match("^[0-9]{4}-[0-1][0-9]-[0-9]{2}$", f"{loanDate}"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid loan date format",
        )
    if not re.match("^[0-9]{4}-[0-1][0-9]-[0-9]{2}$", f"{returnDate}"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid loan date format",
        )
    success = await loans_use_case.delete_all_loan_use_case(loanDate, returnDate, book_id, adherent_id)
    if success:
        return  # HTTP 204 No Content
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="loan not found"
    )