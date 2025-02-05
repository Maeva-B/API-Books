from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.database import authors_collection
from app.schemas import Author, AuthorCreate

router = APIRouter()

@router.get("/{author_id}", response_model=Author)
async def get_author(author_id: str):
    """
    Retrieves a specific author based on its MongoDB identifier.
    Example URL: GET http://localhost/authors/67a391a4198cd394f628c25f
    """
    try:
        oid = ObjectId(author_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid author ID format")
    
    author = await authors_collection.find_one({"_id": oid})
    if author:
        # Convert the MongoDB ObjectId to string and assign it to 'id'
        author["id"] = str(author["_id"])
        return author
    raise HTTPException(status_code=404, detail="Author not found")
