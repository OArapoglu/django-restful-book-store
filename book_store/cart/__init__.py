"""
Cart App

This Django app handles the shopping cart functionality for the bookstore API.
Authenticated users can add books to their cart and proceed to a simulated checkout process.
The app ensures that only available books (based on stock) can be added to the cart and handles race conditions to
prevent multiple users from buying the same book when the stock is limited. It also includes logic to 'release'
books from a user's cart if not purchased within 30 minutes, making them available again for other users.
"""
