"""Define API model."""

from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from enum import Enum

class PyObjectId(ObjectId):
    """ Validation Class to ensure model fiabilty """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        """Validate an instance"""
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}


# Schemas for authors
class AuthorBase(BaseModel):
    """Author base class"""

    first_name: str
    last_name: str
    email: str
    nationality: str

class AuthorCreate(AuthorBase):
    """Author creation class"""
    pass

class Author(AuthorBase):
    """Author base class config"""

    id: Optional[PyObjectId] = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Schemas for books
class BookBase(BaseModel):
    """Book base class"""

    title: str
    description: Optional[str] = None

class BookCreate(BookBase):
    """Book creation class"""

    author_id: str

class Book(BookBase):
    """Book base class config"""

    id: Optional[PyObjectId] = Field(alias="_id")
    author_id: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Schemas for loan
class LoanBase(BaseModel):
    """Loan base class"""
    loanDate: date
    returnDate : date

class LoanCreate(LoanBase):
    """Loan creation class"""

    book_id : str
    adherent_id : str

class Loan(LoanBase):
    """Loan base class config"""

    id: Optional[PyObjectId] = Field(alias="_id")
    book_id : str
    adherent_id : str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# Enum for the adherent role
class RoleEnum(str, Enum):
    """User role enumeration"""

    professor = "professor"
    librarian = "librarian"
    student = "student"

# Schemas for adherents (members)
class AdherentBase(BaseModel):
    """Adherent base class"""

    first_name: str
    last_name: str
    membership_number: str
    login: str
    password: str  # Hashed password !!!!
    role: RoleEnum

class AdherentCreate(AdherentBase):
    """Adherent creation class"""
    pass

class Adherent(AdherentBase):
    """Adherent base class config"""
    id: Optional[PyObjectId] = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
