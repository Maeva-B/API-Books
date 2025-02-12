from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.database import adherents_collection
from app.schemas import Adherent, AdherentCreate
from typing import List, Optional
from passlib.context import CryptContext
from app.schemas import LoginRequest, Token
from app.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

###############################
# CRUD operations for adherents
###############################


# For display, the best practice is not to return the password,
# even hashed, in the API response
@router.get("/{adherent_id}", response_model=Adherent)
async def get_adherent(adherent_id: str):
    """
    Retrieves a specific adherent based on its MongoDB identifier.

    Example URL: GET http://localhost/adherents/67a391a4198cd394f628c25f
    """
    try:
        oid = ObjectId(adherent_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid adherent ID format")

    adherent = await adherents_collection.find_one({"_id": oid})
    if adherent:
        adherent["id"] = str(adherent["_id"])
        # Remove the password field before returning the adherent
        adherent.pop("password", None)
        return adherent
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Adherent not found")


@router.get("/", response_model=List[Adherent])
async def get_adherents(
    role: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    """
    Retrieves all adherents with optional filtering by role and pagination.

    Example URL:
      GET http://localhost/adherents?role=professor&skip=0&limit=10

    Skip (default 0): Indicates the number of adherents to skip from the beginning of the result set.

    Limit (default 10): Indicates the maximum number of adherents to return.
    """
    
    # Build query based on the optional role parameter
    query = {}
    if role:
        query["role"] = role

    adherents_cursor = adherents_collection.find(query).skip(skip).limit(limit)
    adherents = await adherents_cursor.to_list(length=limit)
    for adherent in adherents:
        # Convert the MongoDB ObjectId to string and assign it to 'id'
        adherent["id"] = str(adherent["_id"])
        # Remove the password field before returning the adherent
        adherent.pop("password", None)
    if adherents:
        return adherents
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No adherents found")


@router.post("/", response_model=Adherent, status_code=status.HTTP_201_CREATED)
async def create_adherent(adherent: AdherentCreate):
    """
    Creates a new adherent.

    Example URL:
      POST http://localhost/adherents

    Example payload:
      {
          "first_name": "Alice",
          "last_name": "Smith",
          "membership_number": "M12345",
          "login": "alice_smith",
          "password": "plain_text_password",
          "role": "student"
      }
    """
    adherent_doc = adherent.dict()

    # Hash the password before storing it
    adherent_doc["password"] = pwd_context.hash(adherent_doc["password"])
    result = await adherents_collection.insert_one(adherent_doc)
    adherent_doc["id"] = str(result.inserted_id)

    # Remove the hashed password from the response
    adherent_doc.pop("password", None)
    return adherent_doc


@router.put("/{adherent_id}", response_model=Adherent)
async def update_adherent(adherent_id: str, adherent: AdherentCreate):
    """
    Updates an existing adherent.

    Example URL: PUT http://localhost/adherents/67a391a4198cd394f628c25f

    Example payload:
      {
          "first_name": "Alice",
          "last_name": "Smith",
          "membership_number": "M12345",
          "login": "alice_smith",
          "password": "hashed_password",
          "role": "student"
      }
    """
    try:
        oid = ObjectId(adherent_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid adherent ID format")

    adherent_doc = adherent.dict()
    update_result = await adherents_collection.update_one({"_id": oid}, {"$set": adherent_doc})

    if update_result.modified_count == 1:
        updated_adherent = await adherents_collection.find_one({"_id": oid})
        if updated_adherent:
            updated_adherent["id"] = str(updated_adherent["_id"])
            return updated_adherent

    existing_adherent = await adherents_collection.find_one({"_id": oid})
    if not existing_adherent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Adherent not found")

    existing_adherent["id"] = str(existing_adherent["_id"])
    return existing_adherent


@router.delete("/{adherent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_adherent(adherent_id: str):
    """
    Deletes an existing adherent.

    Example URL: DELETE http://localhost/adherents/67a391a4198cd394f628c25f
    """
    try:
        oid = ObjectId(adherent_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid adherent ID format")

    result = await adherents_collection.delete_one({"_id": oid})
    if result.deleted_count == 1:
        return  # HTTP 204 No Content
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Adherent not found")


###############################


# Authentication
# This endpoint is used to authenticate an adherent and return a JWT token

@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    """
    Authenticates an adherent with login and password and returns a JWT token.

    Example URL: POST http://localhost/adherents/login

    Example payload:
    {
        "login": "toto",
        "password": "toto"
    }
    """
    # Look for the adherent with the provided login
    adherent = await adherents_collection.find_one({"login": login_request.login})
    if not adherent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect login or password"
        )

    # Verify the password against the hashed value stored in the database
    if not pwd_context.verify(login_request.password, adherent["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect login or password"
        )

    # Create the JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": login_request.login, "adherent_id": str(adherent["_id"])},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
