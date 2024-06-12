"""
Book App

This Django app manages the 'Book' entities for the bookstore API.
It supports CRUD operations on books by administrators.
Each book has attributes like title, year published, author, price, and category.
Books are linked to specific categories and have a stock count. Sold-out books are not listed and cannot be purchased.
The app also includes features to list and filter books, including multi-category filtering, accessible to
both anonymous and authenticated users. The app is designed to handle a large inventory of 10,000+ books,
ensuring performance and scalability.
"""
