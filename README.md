# Arbuz Marketplace

## Project Overview

Arbuz is a marketplace web application built with Django for the backend and vanilla JavaScript, HTML, and CSS for the frontend. This project was developed as a final project for a Backend course during university studies. It allows users to browse products, add them to their basket, and make purchases. The admin has a dedicated page to manage the products.

## Key Features

- **User Functionality:**
  - Browse products available in the marketplace.
  - Add products to the basket.
  - Purchase products.

- **Admin Functionality:**
  - Manage products through an admin dashboard.
  - Create, update, and delete products and users.

- **Database:**
  - Uses SQLite for data storage.

## Technologies Used

- **Backend:**
  - Django: Python-based web framework for building the backend.
  
- **Frontend:**
  - JavaScript: For client-side interactions.
  - HTML & CSS: For structuring and styling the web pages.
  
- **Database:**
  - SQLite: Lightweight database used for storing data.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Django 3.2 or higher

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/arbuz.git
   cd arbuz

   Create a Virtual Environment:

### python -m venv venv
### source venv/bin/activate 
On Windows use 
### source venv\Scripts\activate

Install Dependencies:
### pip install -r requirements.txt

Apply Migrations:
### python manage.py migrate

Create a Superuser (for Admin):
### python manage.py createsuperuser

Run the Development Server:
### python manage.py runserver

### Access the Application:
User Interface: http://localhost:8000

Usage
### For Users:
Visit the homepage to browse products.
Add items to your basket and proceed to checkout to make a purchase.

### For Admins:
Log in to the admin interface to manage products.
You can create, update, and delete products and users from this interface.
