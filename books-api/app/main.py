from fastapi import FastAPI
# from app.endpoints import books, authors

app = FastAPI(
    title="Books API",
    description="API to manage books and their authors",
    version="1.0.0"
)

# Test endpoint to verify that the API is working
@app.get("/")
def read_root():
    return {"message": "API is up and running!"}

# app.include_router(books.router, prefix="/books", tags=["Books"])
# app.include_router(authors.router, prefix="/authors", tags=["Authors"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)