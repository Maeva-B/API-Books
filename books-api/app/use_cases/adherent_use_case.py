from app.repositories import adherent_repository
from app.schemas import AdherentCreate
from passlib.context import CryptContext
from datetime import timedelta
from app.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

async def get_adherent_use_case(adherent_id: str) -> dict:
    adherent = await adherent_repository.find_by_id(adherent_id)
    if adherent:
        adherent["id"] = str(adherent["_id"])
        adherent.pop("password", None)
    return adherent

async def list_adherents_use_case(role: str = None, skip: int = 0, limit: int = 10) -> list:
    query = {}
    if role:
        query["role"] = role
    adherents = await adherent_repository.find_all(query, skip, limit)
    for adh in adherents:
        adh["id"] = str(adh["_id"])
        adh.pop("password", None)
    return adherents

async def create_adherent_use_case(adherent_data: AdherentCreate) -> dict:
    adherent_doc = adherent_data.dict()
    # Hachage du mot de passe
    adherent_doc["password"] = pwd_context.hash(adherent_doc["password"])
    inserted_id = await adherent_repository.insert_adherent(adherent_doc)
    adherent_doc["id"] = inserted_id
    adherent_doc.pop("password", None)
    return adherent_doc



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_adherent_use_case(adherent_id: str) -> dict:
    adherent = await adherent_repository.find_by_id(adherent_id)
    if adherent:
        adherent["id"] = str(adherent["_id"])
        adherent.pop("password", None)
    return adherent

async def list_adherents_use_case(role: str = None, skip: int = 0, limit: int = 10) -> list:
    query = {}
    if role:
        query["role"] = role
    adherents = await adherent_repository.find_all(query, skip, limit)
    for adh in adherents:
        adh["id"] = str(adh["_id"])
        adh.pop("password", None)
    return adherents

async def create_adherent_use_case(adherent_data: AdherentCreate) -> dict:
    adherent_doc = adherent_data.dict()
    # Hachage du mot de passe
    adherent_doc["password"] = pwd_context.hash(adherent_doc["password"])
    inserted_id = await adherent_repository.insert_adherent(adherent_doc)
    adherent_doc["id"] = inserted_id
    adherent_doc.pop("password", None)
    return adherent_doc

async def update_adherent_use_case(adherent_id: str, adherent_data: AdherentCreate) -> dict:
    adherent_doc = adherent_data.dict()
    # Si le mot de passe est envoyé, on le hache
    if "password" in adherent_doc and adherent_doc["password"]:
        adherent_doc["password"] = pwd_context.hash(adherent_doc["password"])
    modified_count = await adherent_repository.update_adherent(adherent_id, adherent_doc)
    if modified_count == 1:
        updated_adherent = await adherent_repository.find_by_id(adherent_id)
        if updated_adherent:
            updated_adherent["id"] = str(updated_adherent["_id"])
            updated_adherent.pop("password", None)
            return updated_adherent
    # Si aucune modification n'a été effectuée, on retourne l'adhérent existant (s'il existe)
    existing_adherent = await adherent_repository.find_by_id(adherent_id)
    if existing_adherent:
        existing_adherent["id"] = str(existing_adherent["_id"])
        existing_adherent.pop("password", None)
    return existing_adherent

async def delete_adherent_use_case(adherent_id: str) -> bool:
    deleted_count = await adherent_repository.delete_adherent(adherent_id)
    return deleted_count == 1

async def login_use_case(login: str, password: str) -> dict:
    adherent = await adherent_repository.find_by_login(login)
    if not adherent:
        return None
    if not pwd_context.verify(password, adherent["password"]):
        return None
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": login, "adherent_id": str(adherent["_id"])},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



async def get_loans_by_adherent_use_case(adherent_id: str) -> list:
    loans = await adherent_repository.find_loans_by_adherent(adherent_id)

    for loan in loans:
        loan["_id"] = str(loan["_id"])
        loan["book_id"] = str(loan["book_id"])
        loan["adherent_id"] = str(loan["adherent_id"])

    return loans