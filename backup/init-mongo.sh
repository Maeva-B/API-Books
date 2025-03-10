#!/bin/bash
echo "📥 Importing data into MongoDB..."
mongorestore --host localhost --port 27017 --db books_api /docker-entrypoint-initdb.d/books_api
echo "✅ MongoDB initialization complete!"
