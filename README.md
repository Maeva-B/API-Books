# API-Books

## Project Objective

This project aims to develop a REST API for managing books and authors using **FastAPI**. The API allows you to perform CRUD operations (Create, Read, Update, Delete) on two types of objects:

- **Books**
- **Authors**

The main features include:

- **Pagination** of results for GET requests.
- **Filtering** books by title (and potentially by other criteria).
- **Hierarchical navigation**: access an author's books via a URL such as `/authors/{author_id}/books`.
- **Automatically generated OpenAPI documentation** (accessible via Swagger or Redoc).
- **Validation** of inputs and outputs using Pydantic.
- **Unit tests** to ensure code quality.
- **Containerization** with Docker for simplified local deployment.

---

## Installation

### Prerequisites

- Python 3.10 or higher (if you wish to run the application locally without Docker).
- Docker and Docker Compose (for containerized execution).
- Git

### Cloning the Repository

Clone the Git repository and navigate to the project directory:

```bash
git clone https://github.com/Maeva-B/API-Livres.git
cd API-Livres
```

### Installation via pip

1. **Create and activate a virtual environment** (optional but recommended):

   - On Linux/macOS:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

2. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

### Local Execution with Uvicorn

From the project root directory, run:

```bash
cd books-api
uvicorn app.main:app --reload
```

The application will then be accessible at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Execution with Docker

To run the application using Docker, use Docker Compose:

```bash
docker-compose up --build
```

The API will be accessible at [http://localhost:8000](http://localhost:8000)

---

## API Documentation

FastAPI automatically generates interactive documentation, accessible at:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Tests

To run the unit tests, you can use **pytest**. Ensure that `pytest` is installed, then run:

```bash
pytest
```