// Select or create the "books_api" database
use books_api;

// Insert several documents into the “books” collection
db.books.insertMany([
  { title: "Le Petit Prince", description: "Un conte philosophique", author_id: "1234567890abcdef12345678" },
  { title: "1984", description: "Roman dystopique", author_id: "abcdef1234567890abcdef12" }
]);

// Insert multiple documents into the “authors” collection
db.authors.insertMany([
  { name: "Antoine de Saint-Exupéry" },
  { name: "George Orwell" }
]);
