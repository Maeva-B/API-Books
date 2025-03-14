from app.repositories import loans_repository
from app.schemas import LoanCreate, ObjectId


async def get_loan_use_case(loan_id: str) -> dict:
    loan = await loans_repository.find_by_id(loan_id)
    if loan:
        loan["id"] = str(loan["_id"])
        loan["book_id"] = str(loan["book_id"])
        loan["adherent_id"] = str(loan["adherent_id"])
    return loan


async def list_loans_use_case(
    loanDate: str = None,
    returnDate: str = None,
    book_id: str = None,
    adherent_id: str = None,
    skip: int = 0, limit: int = 10
) -> list:
    query = {}
    if loanDate:
        query["loanDate"] = loanDate
    if returnDate:
        query["returnDate"] = returnDate
    if book_id:
        query["book_id"] = ObjectId(book_id)
    if adherent_id:
        query["adherent_id"] = ObjectId(adherent_id)

    loans = await loans_repository.find_all(query, skip, limit)
    for loan in loans:
        loan["id"] = str(loan["_id"])
        loan["book_id"] = str(loan["book_id"])
        loan["adherent_id"] = str(loan["adherent_id"])
    return loans


async def create_loan_use_case(loan_data: LoanCreate) -> dict:
    loan_doc = loan_data.dict()
    loan_doc["loanDate"] = loan_doc["loanDate"].isoformat()
    loan_doc["returnDate"] = (
        loan_doc["returnDate"].isoformat() if loan_doc["returnDate"] else None
    )

    loan_doc["book_id"] = ObjectId(loan_data.book_id)
    loan_doc["adherent_id"] = ObjectId(loan_data.adherent_id)

    inserted_id = await loans_repository.insert_loan(loan_doc)
    loan_doc["_id"] = str(inserted_id)
    loan_doc["book_id"] = str(loan_doc["book_id"])
    loan_doc["adherent_id"] = str(loan_doc["adherent_id"])

    return loan_doc


async def update_loan_use_case(loan_id: str, loan_data: LoanCreate) -> dict:
    loan_doc = loan_data.dict()
    loan_doc["loanDate"] = loan_doc["loanDate"].isoformat()
    loan_doc["returnDate"] = loan_doc["returnDate"].isoformat()

    modified_count = await loans_repository.update_loan(loan_id, loan_doc)

    if modified_count == 1:
        updated_loan = await loans_repository.find_by_id(loan_id)
        if updated_loan:
            updated_loan["id"] = str(updated_loan["_id"])
            updated_loan["book_id"] = str(updated_loan["book_id"])
            updated_loan["adherent_id"] = str(updated_loan["adherent_id"])
            return updated_loan
    existing_loan = await loans_repository.find_by_id(loan_id)
    if existing_loan:
        existing_loan["id"] = str(existing_loan["_id"])
        existing_loan["book_id"] = str(existing_loan["book_id"])
        existing_loan["adherent_id"] = str(existing_loan["adherent_id"])
        return existing_loan
    return None


async def delete_loan_use_case(loan_id: str) -> bool:
    deleted_count = await loans_repository.delete_loan(loan_id)
    return deleted_count == 1


async def delete_all_loan_use_case(
    loanDate: str = None,
    returnDate: str = None,
    book_id: str = None,
    adherent_id: str = None,
) -> bool:
    query = {}
    if loanDate:
        query["loanDate"] = loanDate
    if returnDate:
        query["returnDate"] = returnDate
    if book_id:
        query["book_id"] = ObjectId(book_id)
    if adherent_id:
        query["adherent_id"] = ObjectId(adherent_id)

    deleted_count = await loans_repository.delete_all_loan(query)
    return deleted_count >= 1
