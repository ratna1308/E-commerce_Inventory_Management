# Inventory Management System

## More About Project
This is a simple Inventory Management System built with **Python (Flask, SQLAlchemy & SQLite)**. The system allows users to:
- **Manage Products & Categories** (Add, Update, Delete)
- **Auto-generate Product & Category IDs**
- **Select categories via dropdown while adding products**
- **View all products in a structured format**

## Features & Implementation
### 1. **Auto-Generated IDs**
- **Category ID**: Automatically assigned when a new category is added.
- **Product ID**: Generated dynamically based on category prefix.

### 2. **Dropdown for Selecting Categories**
- Users can select existing categories while adding a product.
- Ensures correct category association in the database.

### 3. **CRUD Functionality**
- **Categories:** Add, View, and Delete categories.
- **Products:** Add, View, Update (Price & Quantity), and Delete products.

### 4. **Structured Product View**
- Displays product details in a professional format.
- Uses a JSON response to show product details in a clean one-line format.

## Testing Strategy
### 1. **Manual Testing**
- Verify category & product addition, deletion, and updates.
- Check dropdown selection for category while adding products.
- Ensure correct data retrieval and display format.

### 2. **Edge Case Handling**
- Prevents duplicate category names.
- Ensures product IDs remain unique.
- Handles incorrect data input (e.g., non-numeric price values).

## Future Enhancements
- **Search & Filter Products**
- **Export Inventory Data (CSV/Excel)**
- **User Authentication & Role-Based Access**



---

# E-commerce Inventory Management

## Overview
This is a simple Inventory Management System built with **Python (Flask, SQLAlchemy, and SQLite)**. The system allows users to:
- **Manage Products & Categories** (Add, Update, Delete)
- **Auto-generate Product & Category IDs**
- **Select categories via dropdown while adding products**
- **View all products in a structured format**

## Folder Structure
```
E-commerce-Inventory-Management/
│-- app/
│   │-- models.py         # Database models
│   |-- inventory.db      # SQLite database
│   │-- routes.py         # API routes
│-- env/                  # Virtual environment
│-- README.md             # Documentation
│-- requirements.txt      # Dependencies
│-- test_inventory.py     # Test cases
```

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ecommerce-inventory.git
   cd ecommerce-inventory
   ```
2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app/routes.py
   ```

## API Endpoints
### 1. Categories
- **Create a Category**
  ```http
  POST /categories/
  Content-Type: application/json
  {
      "name": "Electronics",
      "description": "Electronic gadgets and devices"
  }
  ```
- **Get All Categories**
  ```http
  GET /categories/
  ```

### 2. Products
- **Create a Product**
  ```http
  POST /products/
  Content-Type: application/json
  {
      "name": "Laptop",
      "price": 1200.99,
      "quantity": 10,
      "category_id": 1
  }
  ```
- **Get All Products**
  ```http
  GET /products/
  ```
- **Update Product Quantity & Price**
  ```http
  PUT /products/{product_id}/
  Content-Type: application/json
  {
      "price": 1100.99,
      "quantity": 15
  }
  ```

  
# Factory Pattern (Best Choice for Core Functionality)
The Factory Pattern is essential for efficiently managing the creation of Product and Category objects. It helps keep the code clean and scalable.

# Strategy Pattern (Useful for Pricing & Discount Logic)
This pattern is useful when we need to modify Product Pricing or apply different Discount Strategies.

It provides flexible code that allows us to change discount strategies at runtime.

If you need to implement multiple discount policies (e.g., 10% seasonal discount, 20% clearance discount), this pattern is highly effective.

# Observer Pattern (Useful for Notifications)
This pattern is useful for sending notifications when a Product is added, updated, or removed.

If  building a GUI, the Observer Pattern can be used to automatically update the UI whenever changes occur.

If you want to integrate an Email/SMS Notification System, the Observer Pattern is the right choice.


## Testing
To run tests:
```bash
pytest test_inventory.py
```

### Example API Calls
- **Get a particular product**: `GET http://127.0.0.1:5000/products/P001`
- **Get all products**: `GET http://127.0.0.1:5000/products/`
- **Get all categroies**: `http://127.0.0.1:5000/categories`
- **Get particular categroie**: `http://127.0.0.1:5000/categories/Accessories`

- **POST    Create products**: `GET http://127.0.0.1:5000/products/`
- **PUT     Update product**: `http://127.0.0.1:5000/products/P100001`
- **DELETE  Delete_product_by_id**: `http://127.0.0.1:5000/products/P100001`
- **DELETE  Delete_category_by_name**: `http://127.0.0.1:5000/categories/Accessories`


## 
Developed by [Ratna Sonawane].
