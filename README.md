# API-Books

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

## Project Objective

This project aims to develop a REST API for managing books and authors using **FastAPI**. The API enables CRUD operations (Create, Read, Update, Delete) on two types of objects:

- **Books**
- **Authors**
- **Adherents**
- **Loans**

### Key Features

- **Pagination** of results for GET requests.
- **Filtering** books by title (and potentially by other criteria).
- **Hierarchical navigation**: Access an author's books via a URL such as `/authors/{author_id}/books`.
- **OpenAPI documentation** (accessible via Swagger UI or Redoc).
- **Input and output validation** using Pydantic.
- **Unit tests** to ensure code quality.
- **Linters** to maintain clean and consistent code.
- **Containerization** with Docker for simplified local deployment.

---

## Installation

### Prerequisites

- **Python 3.10** or higher (if running locally without Docker).
- **Docker** and **Docker Compose** (for containerized execution).
- **Git**

### Cloning the Repository

```bash
git clone https://github.com/Maeva-B/API-Livres.git
cd API-Livres
```

### Installing Dependencies via pip

1. **Create and Activate a Virtual Environment** (optional but recommended):

   - **On Linux/macOS:**

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - **On Windows:**

     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

2. **Install the Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

### Installing and Running MongoDB

#### On macOS (using Homebrew):

```bash
brew tap mongodb/brew
brew install mongodb-community@6.0
brew services start mongodb-community@6.0
```

#### On Windows:

1. Download the MongoDB Community Edition MSI installer from the [MongoDB Download Center](https://www.mongodb.com/try/download/community).
2. Follow the installation instructions and install MongoDB as a Windows service.
3. Verify installation:

   ```cmd
   mongod --version
   ```

4. Create the database directory if it does not exist:

   ```cmd
   mkdir C:\data\db
   ```

5. Start MongoDB:

   ```cmd
   net start MongoDB
   ```

6. Open a terminal and run MongoDB server:

   ```cmd
   mongod
   ```

7. Open another terminal and connect with mongosh:

   ```cmd
   mongosh
   ```

---

## Running the Application

### Local Execution with Uvicorn

```bash
cd books-api
uvicorn app.main:app --reload
```

API will be accessible at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Execution with Docker

```bash
docker-compose up --build
```

API will be accessible at: [http://localhost:8000](http://localhost:8000)

---

## Database Initialization

### Automatic Initialization

If the database initialization via Docker fails, you can manually set it up using the provided backup and scripts located in:

```
API-Livres/backup
```

### Manual Initialization

Create an initialization file (`init.js`) with the following:

```js
use books_api;

db.books.insertMany([
  { title: "Le Petit Prince", description: "A philosophical tale", author_id: "1234567890abcdef12345678" },
  { title: "1984", description: "A dystopian novel", author_id: "abcdef1234567890abcdef12" }
]);

db.authors.insertMany([
  { name: "Antoine de Saint-Exupéry" },
  { name: "George Orwell" }
]);
```

Then, run:

```bash
mongosh < init.js
```

---

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Tests and Code Quality


### Running API Tests

The API tests are available on **Postman** and can be accessed via the following link:

🔗 [Postman Collection - API Books](https://polytech-4256.postman.co/workspace/Polytech-Workspace~61f6f57c-8247-42f8-8994-859b0c62338e/request/19694654-b2023800-c2d4-4df6-b392-a7b96b4a4a42?action=share&creator=19694654&ctx=documentation)

To execute the tests:

1. Open **Postman** (or use the web version with Postman Agent installed).
2. Import the provided **Postman Collection**.
3. Ensure the API is running (`uvicorn` or Docker).
4. Run the collection or individual requests to validate API behavior.

#### Troubleshooting:

- If the provided link does not work, you can rejoin our **Postman team workspace** using the following invite link:  
  🔗 **[Join the Team](https://app.getpostman.com/join-team?invite_code=37fdca8521b31c03c0c384b1cb3dd8810cd474e0ea16e98cac72abc404d796ff)**


These tests cover various endpoints to ensure the correct functionality of CRUD operations.




### Running Linters

We use **Flake8**, **Black**, and **isort** to enforce code quality. Linters are also automatically executed in a GitHub Action workflow, and must pass before merging into the `main` branch.

To run them locally:

```bash
flake8 books-api  # Check for Python syntax and style errors
black books-api   # Auto-format Python code
isort books-api   # Sort imports properly
```


---

## Additional Tools

### Install Postman (for API Testing)

1. Download the installer from the [Postman Download Center](https://www.postman.com/downloads/).
2. Follow the installation steps.
3. Install the Postman Agent if using the web version.


