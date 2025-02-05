from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.database import adherents_collection  # Ensure this is defined in your database module
from app.schemas import Adherent, AdherentCreate  # Ensure the Adherent schema is defined

router = APIRouter()

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
