from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.database import adherents_collection
from app.schemas import Adherent, AdherentCreate
from typing import List, Optional

router = APIRouter()


###############################
# CRUD operations for adherents
###############################

@router.get("/{adherent_id}", response_model=Adherent)
async def get_adherent(adherent_id: str):
    """
    Retrieves a specific adherent based on its MongoDB identifier.
    Example URL: GET http://localhost/adherents/67a3947a198cd394f628c263
    """
    try:
        oid = ObjectId(adherent_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid adherent ID format")
    
    adherent = await adherents_collection.find_one({"_id": oid})
    if adherent:
        # Convert the MongoDB ObjectId to string and assign it to 'id'
        adherent["id"] = str(adherent["_id"])
        return adherent
    raise HTTPException(status_code=404, detail="Adherent not found")

@router.get("/", response_model=List[Adherent])
async def get_adherents():
    """
    Retrieves all adherents.

    Example URL:
      GET http://localhost/adherents
    """
    adherents_cursor = adherents_collection.find()
    adherents = await adherents_cursor.to_list(length=100)
    for adherent in adherents:
        adherent["id"] = str(adherent["_id"])
    if adherents:
        return adherents
    raise HTTPException(status_code=404, detail="No adherents found")


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
          "password": "hashed_password",
          "role": "student"
      }
    """
    adherent_doc = adherent.dict()
    result = await adherents_collection.insert_one(adherent_doc)
    adherent_doc["id"] = str(result.inserted_id)
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid adherent ID format")
    
    adherent_doc = adherent.dict()
    update_result = await adherents_collection.update_one({"_id": oid}, {"$set": adherent_doc})
    
    if update_result.modified_count == 1:
        updated_adherent = await adherents_collection.find_one({"_id": oid})
        if updated_adherent:
            updated_adherent["id"] = str(updated_adherent["_id"])
            return updated_adherent
    
    existing_adherent = await adherents_collection.find_one({"_id": oid})
    if not existing_adherent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adherent not found")
    
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid adherent ID format")
    
    result = await adherents_collection.delete_one({"_id": oid})
    if result.deleted_count == 1:
        return  # HTTP 204 No Content
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Adherent not found")