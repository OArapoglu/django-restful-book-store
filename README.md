# README for Django RESTful API Project: Book Store

## Project Overview

**Book Store** is a Django-based RESTful API project designed to manage an online bookstore. This project consists of five primary apps: `account`, `book`, `category`, `cart`. The project uses Python's virtual environment (`venv`) for dependency management and features Swagger and Redoc for API documentation.

## Features

- API Documentation with Swagger and Redoc.
- RESTful API endpoints for managing books, categories, accounts, and carts.
- User authentication and authorization.
- Scalability to support a large number of books.

## API Documentation

The API documentation is auto-generated using `drf_yasg`. It provides a clear and interactive documentation interface for all available API endpoints.

- **Swagger UI**: Access the Swagger documentation at `http://localhost:8000/swagger/`.
- **Redoc**: Access the Redoc documentation at `http://localhost:8000/redoc/`.

These interfaces allow you to explore the API, send requests, and view responses directly from your browser.

## Getting Started

1. **Setup Virtual Environment**:
   - Create a virtual environment: `python -m venv venv`
   - Activate the environment:
     - Windows: `venv\Scripts\activate`
     - Unix/MacOS: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

2. **Initialize the Database**:
   - Run migrations: `python manage.py migrate`

3. **Running the Server**:
   - Start the Django server: `python manage.py runserver`

4. **Accessing API Documentation**:
   - Swagger UI: `http://localhost:8000/swagger/`
   - Redoc: `http://localhost:8000/redoc/`
