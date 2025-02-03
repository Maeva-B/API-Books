from pydantic import BaseModel
from typing import Optional

# Schemes for authors
class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True

# Schemes for books
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None

class BookCreate(BookBase):
    author_id: int

class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
