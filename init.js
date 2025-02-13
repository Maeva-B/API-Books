use books_api;

db.books.drop();
db.authors.drop();
db.adherents.drop();
db.loans.drop();

const author1Id = ObjectId();
const author2Id = ObjectId();
const author3Id = ObjectId();
const author4Id = ObjectId();

db.authors.insertMany([
  { 
    _id: author1Id,
    first_name: "George", 
    last_name: "Orwell", 
    email: "orwell@example.com", 
    nationality: "British" 
  },
  { 
    _id: author2Id,
    first_name: "Jane", 
    last_name: "Austen", 
    email: "austen@example.com", 
    nationality: "British" 
  },
  { 
    _id: author3Id,
    first_name: "Ernest", 
    last_name: "Hemingway", 
    email: "hemingway@example.com", 
    nationality: "American" 
  },
  { 
    _id: author4Id,
    first_name: "Mark", 
    last_name: "Twain", 
    email: "twain@example.com", 
    nationality: "American" 
  }
]);

const book1Id  = ObjectId();
const book2Id  = ObjectId();
const book3Id  = ObjectId();
const book4Id  = ObjectId();
const book5Id  = ObjectId();
const book6Id  = ObjectId();

db.books.insertMany([
  {
    _id: book1Id,
    title: "Introduction to Data Science",
    description: "A comprehensive guide to data science principles and applications.",
    location: "Shelf A1",
    label: "Data Science Basics",
    type: "datascience",
    publishDate: "2021-05-15",
    publisher: "Springer",
    language: "English",
    link: "https://example.com/data-science",
    author_id: author1Id
  },
  {
    _id: book2Id,
    title: "Modern Web Development",
    description: "Exploring the latest trends in front-end and back-end web development.",
    location: "Shelf B3",
    label: "Web Technologies",
    type: "web",
    publishDate: "2023-01-20",
    publisher: "O'Reilly",
    language: "English",
    link: "https://example.com/web-development",
    author_id: author2Id
  },
  {
    _id: book3Id,
    title: "Linear Algebra and Its Applications",
    description: "An essential textbook for students and researchers in mathematics.",
    location: "Shelf C2",
    label: "Mathematical Foundations",
    type: "algebra",
    publishDate: "2019-09-10",
    publisher: "Pearson",
    language: "English",
    link: "https://example.com/linear-algebra",
    author_id: author3Id
  },
  {
    _id: book4Id,
    title: "Optimization Techniques in Machine Learning",
    description: "A deep dive into optimization methods used in AI and ML.",
    location: "Shelf D5",
    label: "Advanced Optimization",
    type: "optimization",
    publishDate: "2022-07-12",
    publisher: "MIT Press",
    language: "English",
    link: "https://example.com/optimization-ml",
    author_id: author4Id
  },
  {
    _id: book5Id,
    title: "The Art of Philosophy",
    description: "Exploring fundamental philosophical questions and theories.",
    location: "Shelf E1",
    label: "Philosophy Insights",
    type: "phylosophy",
    publishDate: "2018-03-25",
    publisher: "Oxford University Press",
    language: "French",
    link: "https://example.com/philosophy",
    author_id: author1Id
  },
  {
    _id: book6Id,
    title: "Advanced Machine Learning",
    description: "A comprehensive guide to advanced machine learning techniques.",
    location: "Shelf F1",
    label: "Machine Learning",
    type: "optimization",
    publishDate: "2025-01-15",
    publisher: "MIT Press",
    language: "English",
    link: "https://example.com/advanced-ml",
    author_id: author3Id
  }
]);

const adherent1Id = ObjectId();
const adherent2Id = ObjectId();
const adherent3Id = ObjectId();

db.adherents.insertMany([
  { 
    _id: adherent1Id,
    first_name: "Alice", 
    last_name: "Smith", 
    membership_number: "MEM001", 
    login: "asmith", 
    password: "hashed_password1", 
    role: "professor" 
  },
  { 
    _id: adherent2Id,
    first_name: "Bob", 
    last_name: "Brown", 
    membership_number: "MEM002", 
    login: "bbrown", 
    password: "hashed_password2", 
    role: "librarian" 
  },
  { 
    _id: adherent3Id,
    first_name: "Charlie", 
    last_name: "Davis", 
    membership_number: "MEM003", 
    login: "cdavis", 
    password: "hashed_password3", 
    role: "student" 
  }
]);

db.loans.insertMany([
  { 
    loanDate: "2012-10-10", 
    returnDate: "2012-10-27", 
    book_id: book1Id, 
    adherent_id: adherent1Id  
  },
  { 
    loanDate: "2024-12-10", 
    returnDate: "2024-01-10", 
    book_id: book2Id, 
    adherent_id: adherent1Id  
  },
  { 
    loanDate: "2024-10-06", 
    returnDate: "2024-12-30", 
    book_id: book1Id, 
    adherent_id: adherent2Id  
  },
  { 
    loanDate: "2012-10-10", 
    returnDate: "2012-10-27", 
    book_id: book2Id, 
    adherent_id: adherent1Id  
  },
  { 
    loanDate: "2025-02-01", 
    returnDate: "2025-02-28", 
    book_id: book6Id, 
    adherent_id: adherent3Id  
  }
]);