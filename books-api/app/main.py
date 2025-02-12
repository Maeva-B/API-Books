"""Main program of the API. Manage roots and web server"""

from fastapi import FastAPI
<<<<<<< Updated upstream
from app.endpoints import books, authors, adherents
=======
from app.endpoints import books, authors
from app.controllers import adherent_controller
from fastapi.middleware.cors import CORSMiddleware
>>>>>>> Stashed changes

app = FastAPI(
    title="Books API",
    description="API to manage books and their authors",
    version="1.0.0"
)

app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(authors.router, prefix="/authors", tags=["Authors"])
app.include_router(adherent_controller.router, prefix="/adherents", tags=["Adherents"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
