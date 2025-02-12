"""Main program of the API. Manage roots and web server"""

from fastapi import FastAPI
from app.endpoints import books
from app.controllers import adherent_controller, authors_controller
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Books API",
    description="API to manage books and their authors",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(authors_controller.router, prefix="/authors", tags=["Authors"])
app.include_router(adherent_controller.router, prefix="/adherents", tags=["Adherents"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
