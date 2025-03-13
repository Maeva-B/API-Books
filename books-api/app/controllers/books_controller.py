from typing import List, Optional

from app.schemas import Book, BookCreate, TypeEnum
from app.use_cases import books_use_case
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get(
    "/{book_id}",
    response_model=Book,
    summary="Retrieve an book",
)
async def get_book(book_id: str):
    """
    Retrieves a specific book based on its MongoDB identifier.

    - **book_id**: Unique identifier of the book.

    **Example Request:**
    ```
    GET http://localhost/books/67a36d9a198cd394f628c25c
    ```
    """
    book = await books_use_case.get_book_use_case(book_id)
    if book:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
    )


@router.get(
    "/",
    response_model=List[Book],
    summary="List books",
)
async def get_books(
    title: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    label: Optional[str] = None,
    type: Optional[TypeEnum] = None,
    publishDate: Optional[str] = None,
    publisher: Optional[str] = None,
    language: Optional[str] = None,
    link: Optional[str] = None,
    author_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
):
    """
    Retrieve a list of books with optional filtering.

    - **title**: Filter books by title.
    - **description**: Filter books by description.
    - **location**: Filter books by location in the university library.
    - **label**: Filter books by label.
    - **type**: Filter books by type.
    - **publishDate**: Filter books by publication date.
    - **publisher**: Filter books by publisher.
    - **language**: Filter books by language.
    - **link**: Filter books by link.
    - **author_id**: Filter books by author.
    - **skip**: Number of records to skip.
    - **limit**: Maximum number of records to return.

    **Example Request:**
    ```
    GET http://localhost:8000/books/?title=Introduction%20to%20Data%20Science&location=Shelf%20A1&type=datascience&skip=0&limit=10
    ```
    """
    books = await books_use_case.list_books_use_case(
        title, description, location, label, type, publishDate,
        publisher, language, link, author_id, skip, limit
    )
    if books:
        return books
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No books found"
    )


@router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
)
async def create_book(book: BookCreate):
    """
    Create a new book.

    **Request Body:**
   - **title**: book's title.
    - **description**: book's description.
    - **location**: book's location.
    - **label**: book's label.
    - **type**: book's type.
    - **publishDate**: book's publication date.
    - **publisher**: book's publisher.
    - **language**: book's language.
    - **link**: book's link.
    - **author_id**: book's author.

    **Example Request:**
    ```
    POST /books
    {
        "title": "Introduction to Data Science",
        "description": "This course covers the fundamental concepts of data science, including data analysis, machine learning, and data visualization techniques.",
        "location": "Online",
        "label": "Data Science, Learning",
        "type": "datascience",
        "publishDate": "2025-03-12",
        "publisher": "Tech Academy",
        "language": "English",
        "link": "https://www.techacademy.com/datascience-course",
        "author_id": "67a9d9fb635513c2db4d794d"
    }
    ```
    """
    created_book = await books_use_case.create_book_use_case(book)
    return created_book


@router.put(
    "/{book_id}",
    response_model=Book,
    summary="Update a book",
)
async def update_book(book_id: str, book: BookCreate):
    """
    Update an existing book.

    - **book_id**: Unique identifier of the book to update.

    **Example Request:**
    ```
    PUT /books/60b725f10c9f1e23d8f3a3e9
     {
        "title": "Introduction to Data Science",
        "description": "This course covers the fundamental concepts of data science, including data analysis, machine learning, and data visualization techniques.",
        "location": "Shelf A5",
        "label": "Data Science, Learning",
        "type": "datascience",
        "publishDate": "2025-03-12",
        "publisher": "Tech Academy",
        "language": "English",
        "link": "https://www.techacademy.com/datascience-course",
        "author_id": "67a9d9fb635513c2db4d794d"
    }
    ```
    """
    updated_book = await books_use_case.update_book_use_case(book_id, book)
    if updated_book:
        return updated_book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
    )


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
)
async def delete_book(book_id: str):
    """
    Delete an existing book by its unique identifier.

    **Example Request:**
    ```
    DELETE /books/60b725f10c9f1e23d8f3a3e9
    ```

    **Response:**
    HTTP 204 No Content
    """
    success = await books_use_case.delete_book_use_case(book_id)
    if success:
        return  # HTTP 204 No Content
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
    )


@router.get(
    "/{book_id}/author",
    summary="Retrieve author by book",
)
async def get_author_by_book(book_id: str):
    """
    Retrieve an author linked to a specific book.

    - **book_id**: Unique identifier of the book.

    **Example Request:**
    ```
    GET /books/60b725f10c9f1e23d8f3a3e9/author
    ```
    """
    books = await books_use_case.get_author_by_book_use_case(book_id)
    if books:
        return books
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No author found for this book"
    )
