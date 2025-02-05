from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}


# Schemas for authors
class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    nationality: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: Optional[PyObjectId] = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Schemas for books
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None

class BookCreate(BookBase):
    author_id: str

class Book(BookBase):
    id: Optional[PyObjectId] = Field(alias="_id")
    author_id: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        

# Enum for the adherent role
class RoleEnum(str, Enum):
    professor = "professor"
    librarian = "librarian"
    student = "student" 
        

# Schemas for adherents (members)
class AdherentBase(BaseModel):
    first_name: str
    last_name: str
    membership_number: str
    login: str
    password: str  # Hashed password !!!!
    role: RoleEnum

class AdherentCreate(AdherentBase):
    pass

class Adherent(AdherentBase):
    id: Optional[PyObjectId] = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}