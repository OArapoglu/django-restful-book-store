"""
Account App

This app manages user accounts for the bookstore API.
It handles user registration and authentication using email and password.
The app defines two main types of users: authenticated users and administrators.
While admins have privileges to CRUD categories and books, authenticated users can browse books, add them to their cart,
and perform checkout operations. The app ensures security and data validation for user-related operations.
Admins are assigned only through direct database manipulation.
The app is built to support a user base interacting with a large-scale book inventory.
"""
