// Select or create the "books_api" database
use books_api;

// Insert several documents into the “books” collection
db.books.insertMany([
  {
    "title": "Introduction to Data Science",
    "description": "A comprehensive guide to data science principles and applications.",
    "location": "Shelf A1",
    "label": "Data Science Basics",
    "type": "datascience",
    "publishDate": "2021-05-15",
    "publisher": "Springer",
    "language": "English",
    "link": "https://example.com/data-science",
    "author_id":"6"
  },
  {
    "title": "Modern Web Development",
    "description": "Exploring the latest trends in front-end and back-end web development.",
    "location": "Shelf B3",
    "label": "Web Technologies",
    "type": "web",
    "publishDate": "2023-01-20",
    "publisher": "O'Reilly",
    "language": "English",
    "link": "https://example.com/web-development",
    "author_id":"1"
  },
  {
    "title": "Linear Algebra and Its Applications",
    "description": "An essential textbook for students and researchers in mathematics.",
    "location": "Shelf C2",
    "label": "Mathematical Foundations",
    "type": "algebra",
    "publishDate": "2019-09-10",
    "publisher": "Pearson",
    "language": "English",
    "link": "https://example.com/linear-algebra",
    "author_id":"8"
  },
  {
    "title": "Optimization Techniques in Machine Learning",
    "description": "A deep dive into optimization methods used in AI and ML.",
    "location": "Shelf D5",
    "label": "Advanced Optimization",
    "type": "optimization",
    "publishDate": "2022-07-12",
    "publisher": "MIT Press",
    "language": "English",
    "link": "https://example.com/optimization-ml",
    "author_id":"9"
  },
  {
    "title": "The Art of Philosophy",
    "description": "Exploring fundamental philosophical questions and theories.",
    "location": "Shelf E1",
    "label": "Philosophy Insights",
    "type": "phylosophy",
    "publishDate": "2018-03-25",
    "publisher": "Oxford University Press",
    "language": "French",
    "link": "https://example.com/philosophy",
    "author_id":"7"
  },
  {
    "title": "Classic Literary Works",
    "description": "A collection of timeless literary masterpieces.",
    "location": "Shelf F4",
    "label": "Literary Classics",
    "type": "literary",
    "publishDate": "2015-11-30",
    "publisher": "Penguin Books",
    "language": "English",
    "link": "https://example.com/literary-classics",
    "author_id":"6"
  },
  {
    "title": "Operating System Concepts",
    "description": "An introduction to modern operating system principles.",
    "location": "Shelf G6",
    "label": "System Programming",
    "type": "system",
    "publishDate": "2020-04-18",
    "publisher": "Wiley",
    "language": "English",
    "link": "https://example.com/os-concepts",
    "author_id":"5"
  },
  {
    "title": "Computer Networks: A Systems Approach",
    "description": "A detailed study on networking principles and applications.",
    "location": "Shelf H2",
    "label": "Networking Basics",
    "type": "network",
    "publishDate": "2021-09-05",
    "publisher": "Morgan Kaufmann",
    "language": "English",
    "link": "https://example.com/computer-networks",
    "author_id":"4"
  },
  {
    "title": "Fundamentals of Physics",
    "description": "A comprehensive guide to classical and modern physics.",
    "location": "Shelf I3",
    "label": "Physics Essentials",
    "type": "physic",
    "publishDate": "2017-06-22",
    "publisher": "McGraw-Hill",
    "language": "English",
    "link": "https://example.com/fundamentals-physics",
    "author_id":"3"
  },
  {
    "title": "Principles of Chemistry",
    "description": "An in-depth look at chemical reactions and molecular structures.",
    "location": "Shelf J1",
    "label": "Chemistry Principles",
    "type": "chemistry",
    "publishDate": "2016-12-10",
    "publisher": "Pearson",
    "language": "English",
    "link": "https://example.com/chemistry",
    "author_id":"2"
  },
  {
    "title": "Introduction to Optics",
    "description": "A study on the behavior and properties of light.",
    "location": "Shelf K4",
    "label": "Optical Physics",
    "type": "optic",
    "publishDate": "2018-08-14",
    "publisher": "Cambridge University Press",
    "language": "English",
    "link": "https://example.com/optics",
    "author_id":"1"
  },
  {
    "title": "Electronic Circuits and Applications",
    "description": "A hands-on guide to designing and analyzing electronic circuits.",
    "location": "Shelf L5",
    "label": "Electronics Engineering",
    "type": "electronic",
    "publishDate": "2019-03-29",
    "publisher": "Prentice Hall",
    "language": "English",
    "link": "https://example.com/electronics",
    "author_id":"0"
  }
]
);

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
  { loanDate:"2024-10-06", returnDate: "2024-12-30",book_id:"0", adherent_id:"1"},
  { loanDate:"2012-10-10", returnDate:"2012-10-27", book_id:"1", adherent_id:"0"}, 
]);