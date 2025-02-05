from fastapi import FastAPI
from app.endpoints import books

app = FastAPI(
    title="Books API",
    description="API to manage books and their authors",
    version="1.0.0"
)

app.include_router(books.router, prefix="/books", tags=["Books"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)