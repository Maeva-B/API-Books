# Use the official Python image as a base
FROM python:3.12

# Set the working directory for the API
WORKDIR /

# Copy the requirements.txt file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the API into the container
COPY / .

# Expose the port that FastAPI uses
EXPOSE 8000

# Command to start the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--app-dir", "books-api"]