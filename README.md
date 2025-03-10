# API-Books

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

## Project Objective

This project aims to develop a REST API for managing books and authors using **FastAPI**. The API enables you to perform CRUD operations (Create, Read, Update, Delete) on two types of objects:

- **Books**
- **Authors**

**Key features include:**

- **Pagination** of results for GET requests.
- **Filtering** books by title (and potentially by other criteria).
- **Hierarchical navigation**: Access an author's books via a URL such as `/authors/{author_id}/books`.
- **Automatically generated OpenAPI documentation** (accessible via Swagger UI or Redoc).
- **Input and output validation** using Pydantic.
- **Unit tests** to ensure code quality.
- **Linters** to ensure code quality.
- **Containerization** with Docker for simplified local deployment.


---

## Installation

### Prerequisites

- **Python 3.10** or higher (if you wish to run the application locally without Docker).
- **Docker** and **Docker Compose** (for containerized execution).
- **Git**

### Cloning the Repository

Clone the repository and navigate to the project directory:

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

3. **Install MongoDB (if you haven’t already):**

   - **On macOS (using Homebrew):**

     ```bash
     brew tap mongodb/brew
     brew install mongodb-community@6.0
     ```

   - **On Windows:**

      1. Download the MongoDB Community Edition MSI installer from the [MongoDB Download Center](https://www.mongodb.com/try/download/community).
      2. Run the installer MSI and follow the on-screen instructions.
      3. When prompted, choose to install MongoDB as a Windows service (or configure it to run manually if preferred).
      4. Test the installation with the following command and add its path (C:\Program Files\MongoDB\Server\8.0\bin) to the PATH environment variable if needed. In that case, restart your PC to apply the changes.
            ```cmd
               mongod --version
            ```
      5. Create the Database Directory if the folder does not exist. MongoDB stores data in C:\data\db by default :
            ```cmd
               mkdir C:\data\db
            ```
      6. Download the MongoDB Shell installer (if mongosh is not included) from the [MongoDB Shell Download Center](https://www.mongodb.com/try/download/shell).
      7. Install it and add its path to the PATH environment variable if needed.
      8. After installation, you can start MongoDB via the Services panel or using the following command in Command Prompt (run as Administrator):

         ```cmd
         net start MongoDB
         ```
      You can also open a terminal and run the MongoDB server then, open another terminal to connect with mongosh. 
         ```cmd
         mongod
         ```
         ```cmd
         mongosh
         ```

4. **Install Docker**

Docker is an open platform that wraps our applications from our infrastructure. 

   1. Install Docker Desktop on your local machine (https://docs.docker.com/get-started/introduction/get-docker-desktop/) and complete setup process.

5. **Install Postman App**
   1. Download the installer adapted for your OS from the [Postman Download Center](https://www.postman.com/downloads/).
   2. Run the installer MSI and follow the on-screen instructions.
   3. Install Postman Agent if you use the web version.
      
---

## Running the Application

### Local Execution with Uvicorn

From the project root directory, run:

```bash
cd books-api
uvicorn app.main:app --reload
```

The application will be accessible at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Execution with Docker

To run the application using Docker, execute:

```bash
docker-compose up --build
```

The API will be accessible at: [http://localhost:8000](http://localhost:8000)

---

## Using MongoDB

### Starting MongoDB as a Service

**On macOS (using Homebrew):**

```bash
brew services start mongodb-community@6.0
```

**On Windows:**

If you are using Windows, the process is different. You might need to:

1. Download the MongoDB Community Edition MSI installer from the [MongoDB Download Center](https://www.mongodb.com/try/download/community).
2. Follow the installation instructions.
3. Start MongoDB as a Windows service via the Services panel or using the following command in Command Prompt (run as Administrator):

   ```cmd
   net start MongoDB
   ```
You can also open a terminal and run the MongoDB server.
   ```cmd
     mongod
     ```

### Connecting to MongoDB

1. **Launch the MongoDB Shell:**
Open another terminal to connect with mongosh. 
   ```bash
   mongosh
   ```

### Initialization

You can initialize your database by creating an initialization file. For example, create a file named `init.js` with the following content:

```js
// Select or create the "books_api" database
use books_api;

// Insert sample documents into the "books" collection
db.books.insertMany([
  { title: "Le Petit Prince", description: "A philosophical tale", author_id: "1234567890abcdef12345678" },
  { title: "1984", description: "A dystopian novel", author_id: "abcdef1234567890abcdef12" }
]);

// Insert sample documents into the "authors" collection
db.authors.insertMany([
  { name: "Antoine de Saint-Exupéry" },
  { name: "George Orwell" }
]);
```

To initialize your database using the file:

```bash
mongosh < init.js
```

Alternatively, you can perform the following steps manually:

1. **Create and Select a Database:**

   (This is done implicitly when you insert data. For example:)

   ```js
   use your_api
   ```

2. **Insert Sample Data into a Collection:**

   ```js
   db.books.insertMany([
     { title: "Le Petit Prince", description: "A philosophical tale", author_id: "1234567890abcdef12345678" },
     { title: "1984", description: "A dystopian novel", author_id: "abcdef1234567890abcdef12" }
   ])
   ```

3. **Verify the Inserted Data:**

   ```js
   db.books.find().pretty()
   ```

---

## API Documentation

FastAPI automatically generates interactive API documentation, which you can access at:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Tests

To run the unit tests, ensure **pytest** is installed, then execute:

```bash
pytest
```

## Linters

To run the Pylint linter, ensure **pylint** is installed, then execute:

```bash
pylint books-api
```

For more informations, refer to the documentation : https://docs.pylint.org/run.html
