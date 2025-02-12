// Select or create the "books_api" database
use books_api;

// Insert several documents into the “books” collection
db.books.insertMany([
  { title: "Le Petit Prince", description: "Un conte philosophique", author_id: "1234567890abcdef12345678" },
  { title: "1984", description: "Roman dystopique", author_id: "abcdef1234567890abcdef12" }
]);

// Insert multiple documents into the “authors” collection
db.authors.insertMany([
  { first_name: "George", last_name: "Orwell", email: "orwell@example.com", nationality: "British" },
  { first_name: "Jane", last_name: "Austen", email: "austen@example.com", nationality: "British" },
  { first_name: "Ernest", last_name: "Hemingway", email: "hemingway@example.com", nationality: "American" },
  { first_name: "Mark", last_name: "Twain", email: "twain@example.com", nationality: "American" }
])

db.adherents.insertMany([
  { 
    first_name: "Alice", 
    last_name: "Smith", 
    membership_number: "MEM001", 
    login: "asmith", 
    password: "hashed_password1", 
    role: "professor" 
  },
  { 
    first_name: "Bob", 
    last_name: "Brown", 
    membership_number: "MEM002", 
    login: "bbrown", 
    password: "hashed_password2", 
    role: "librarian" 
  },
  { 
    first_name: "Charlie", 
    last_name: "Davis", 
    membership_number: "MEM003", 
    login: "cdavis", 
    password: "hashed_password3", 
    role: "student" 
  }
]);

db.loans.insertMany([
  { loanDate:"2012-10-10", returnDate:"2012-10-27", book_id:"0", adherent_id:"0"}, 
  {loanDate:"2024-12-10", returnDate:"2025-01-10", book_id:"1", adherent_id:"0"}, 
  { loanDate:"2024-10-06", returnDate: "2024-12-30",book_id:"0", adherent_id:"1"}
]);