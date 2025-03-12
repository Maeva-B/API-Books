from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.schemas import Author, AuthorCreate
from app.use_cases import authors_use_case

router = APIRouter()


@router.get(
    "/{author_id}",
    response_model=Author,
    summary="Retrieve an author",
)
async def get_author(author_id: str):
    """
    Retrieve an author by its unique identifier.

    - **author_id**: Unique identifier of the author.

    **Example Request:**
    ```
    GET /authors/60b725f10c9f1e23d8f3a3e9
    ```
    """
    author = await authors_use_case.get_author_use_case(author_id)
    if author:
        return author
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
    )


@router.get(
    "/",
    response_model=List[Author],
    summary="List authors",
)
async def get_authors(
    name: Optional[str] = None,
    nationality: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
):
    """
    Retrieve a list of authors.

    - **name**: Filter authors by first name or last name.
    - **nationality**: Filter authors by nationality.
    - **skip**: Number of records to skip.
    - **limit**: Maximum number of records to return.

    **Example Request:**
    ```
    GET /authors?name=Alice&nationality=British&skip=0&limit=10
    ```
    """
    authors = await authors_use_case.list_authors_use_case(
        name, nationality, skip, limit
    )
    if authors:
        return authors
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No authors found"
    )


@router.post(
    "/",
    response_model=Author,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new author",
)
async def create_author(author: AuthorCreate):
    """
    Create a new author.

    **Request Body:**
    - **first_name**: Author's first name.
    - **last_name**: Author's last name.
    - **email**: Author's email address.
    - **nationality**: Author's nationality.

    **Example Request:**
    ```
    POST /authors
    {
      "first_name": "Alice",
      "last_name": "Smith",
      "email": "alice@example.com",
      "nationality": "British"
    }
    ```
    """
    created_author = await authors_use_case.create_author_use_case(author)
    return created_author


@router.put(
    "/{author_id}",
    response_model=Author,
    summary="Update an author",
)
async def update_author(author_id: str, author: AuthorCreate):
    """
    Update an existing author.

    - **author_id**: Unique identifier of the author to update.

    **Example Request:**
    ```
    PUT /authors/60b725f10c9f1e23d8f3a3e9
    {
      "first_name": "Alice",
      "last_name": "Smith",
      "email": "alice@example.com",
      "nationality": "British"
    }
    ```
    """
    updated_author = await authors_use_case.update_author_use_case(author_id, author)
    if updated_author:
        return updated_author
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
    )


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an author",
)
async def delete_author(author_id: str):
    """
    Delete an author by its unique identifier.

    **Example Request:**
    ```
    DELETE /authors/60b725f10c9f1e23d8f3a3e9
    ```

    **Response:**
    HTTP 204 No Content
    """
    success = await authors_use_case.delete_author_use_case(author_id)
    if success:
        return  # HTTP 204 No Content
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
    )


@router.get(
    "/{author_id}/books",
    summary="Retrieve books by author",
)
async def get_books_by_author(author_id: str):
    """
    Retrieve all books linked to a specific author.

    - **author_id**: Unique identifier of the author.

    **Example Request:**
    ```
    GET /authors/60b725f10c9f1e23d8f3a3e9/books
    ```
    """
    books = await authors_use_case.get_books_by_author_use_case(author_id)
    if books:
        return books
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No books found for this author"
    )
