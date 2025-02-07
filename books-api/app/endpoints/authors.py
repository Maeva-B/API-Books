from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from app.database import authors_collection
from app.schemas import Author, AuthorCreate
from typing import List, Optional


router = APIRouter()


#############################
# CRUD operations for authors
#############################

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


@router.get("/", response_model=List[Author])
async def get_authors(name: Optional[str] = None, nationality: Optional[str] = None):
    """
    Retrieves all authors with optional filtering by name and nationality.

    Example URL:
      GET http://localhost/authors?name=Alice&nationality=British
    """
    query = {}
    if name:
        query["$or"] = [{"first_name": name}, {"last_name": name}]
    if nationality:
        query["nationality"] = nationality

    authors_cursor = authors_collection.find(query)
    authors = await authors_cursor.to_list(length=100)
    for author in authors:
        # Convert the MongoDB ObjectId to string and assign it to 'id'
        author["id"] = str(author["_id"])
    if authors:
        return authors
    raise HTTPException(status_code=404, detail="No authors found")


@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
async def create_author(author: AuthorCreate):
    """
    Creates a new author.
    
    Example URL:
      POST http://localhost/authors
    
    Example payload:
      {
          "first_name": "Alice",
          "last_name": "Smith",
          "email": "alice@example.com",
          "nationality": "British"
      }
    """
    author_doc = author.dict()
    result = await authors_collection.insert_one(author_doc)
    # Append the generated id to the document.
    author_doc["id"] = str(result.inserted_id)
    # Optionally, remove "_id" if present (since we use "id" for output)
    return author_doc


@router.put("/{author_id}", response_model=Author)
async def update_author(author_id: str, author: AuthorCreate):
    """
    Updates an existing author.
    
    Example URL: PUT http://localhost/authors/67a391a4198cd394f628c25f
    
    Example payload:
    {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "nationality": "British"
    }
    """
    try:
        oid = ObjectId(author_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid author ID format")
    
    author_doc = author.dict()
    update_result = await authors_collection.update_one({"_id": oid}, {"$set": author_doc})
    
    if update_result.modified_count == 1:
        updated_author = await authors_collection.find_one({"_id": oid})
        if updated_author:
            updated_author["id"] = str(updated_author["_id"])
            return updated_author
    
    # Check if the author exists; if not, raise a 404 error.
    existing_author = await authors_collection.find_one({"_id": oid})
    if not existing_author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    
    # If no modifications were made, return the existing author.
    existing_author["id"] = str(existing_author["_id"])
    return existing_author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: str):
    """
    Deletes an existing author.
    Example URL: DELETE http://localhost/authors/67a391a4198cd394f628c25f
    """
    try:
        oid = ObjectId(author_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid author ID format")
    
    result = await authors_collection.delete_one({"_id": oid})
    if result.deleted_count == 1:
        return  # HTTP 204 No Content
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

