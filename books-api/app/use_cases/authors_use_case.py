from app.repositories import authors_repository
from app.schemas import AuthorCreate


async def get_author_use_case(author_id: str) -> dict:
    author = await authors_repository.find_by_id(author_id)
    if author:
        author["id"] = str(author["_id"])
    return author


async def list_authors_use_case(
    name: str = None, nationality: str = None, skip: int = 0, limit: int = 10
) -> list:
    query = {}
    if name:
        query["$or"] = [{"first_name": name}, {"last_name": name}]
    if nationality:
        query["nationality"] = nationality
    authors = await authors_repository.find_all(query, skip, limit)
    for author in authors:
        author["id"] = str(author["_id"])
    return authors


async def create_author_use_case(author_data: AuthorCreate) -> dict:
    author_doc = author_data.dict()
    inserted_id = await authors_repository.insert_author(author_doc)
    author_doc["id"] = inserted_id
    return author_doc


async def update_author_use_case(author_id: str, author_data: AuthorCreate) -> dict:
    author_doc = author_data.dict()
    modified_count = await authors_repository.update_author(author_id, author_doc)
    if modified_count == 1:
        updated_author = await authors_repository.find_by_id(author_id)
        if updated_author:
            updated_author["id"] = str(updated_author["_id"])
            return updated_author
    existing_author = await authors_repository.find_by_id(author_id)
    if existing_author:
        existing_author["id"] = str(existing_author["_id"])
        return existing_author
    return None


async def delete_author_use_case(author_id: str) -> bool:
    deleted_count = await authors_repository.delete_author(author_id)
    return deleted_count == 1


async def get_books_by_author_use_case(author_id: str) -> list:
    books = await authors_repository.find_books_by_author(author_id)
    return books
