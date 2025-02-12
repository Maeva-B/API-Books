from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.schemas import Author, AuthorCreate
from app.use_cases import authors_use_case

router = APIRouter()

@router.get("/{author_id}", response_model=Author)
async def get_author(author_id: str):
    author = await authors_use_case.get_author_use_case(author_id)
    if author:
        return author
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

@router.get("/", response_model=List[Author])
async def get_authors(
    name: Optional[str] = None,
    nationality: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    authors = await authors_use_case.list_authors_use_case(name, nationality, skip, limit)
    if authors:
        return authors
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No authors found")

@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
async def create_author(author: AuthorCreate):
    created_author = await authors_use_case.create_author_use_case(author)
    return created_author

@router.put("/{author_id}", response_model=Author)
async def update_author(author_id: str, author: AuthorCreate):
    updated_author = await authors_use_case.update_author_use_case(author_id, author)
    if updated_author:
        return updated_author
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: str):
    success = await authors_use_case.delete_author_use_case(author_id)
    if success:
        return  # HTTP 204 No Content
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")