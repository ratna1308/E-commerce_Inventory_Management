from flask import Flask, request, jsonify
from models import Inventory, Database
import logging

app = Flask(__name__)

db = Database()
inventory = Inventory(db)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def response(success: bool, message: str, data=None, status_code=200):
    """Helper function to format API responses."""
    response_data = {"success": success, "message": message}
    if data is not None:
        response_data["data"] = data
    return jsonify(response_data), status_code


@app.route('/products', methods=['GET'])
def get_all_products():
    """Retrieve all products"""
    try:
        products = inventory.get_all_products()
        return response(True, "Products retrieved successfully", products)
    except Exception as e:
        logging.error(f"Error fetching products: {str(e)}")
        return response(False, "Internal Server Error", status_code=500)


@app.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    """Retrieve a specific product"""
    product = inventory.get_product(product_id)
    if not product:
        return response(False, "Product not found", status_code=404)
    return response(True, "Product retrieved successfully", product)


@app.route('/categories', methods=['GET'])
def get_all_categories():
    """Retrieve all categories"""
    try:
        categories = inventory.get_all_categories()
        return response(True, "Categories retrieved successfully", categories)
    except Exception as e:
        logging.error(f"Error fetching categories: {str(e)}")
        return response(False, "Internal Server Error", status_code=500)


@app.route('/categories/<string:category_name>', methods=['GET'])
def get_category(category_name):
    """Retrieve a specific category"""
    category = inventory.get_category(category_name)
    if not category:
        return response(False, "Category not found", status_code=404)
    return response(True, "Category retrieved successfully", category)


@app.route('/products', methods=['POST'])
def add_product():
    """Add a new product"""
    data = request.json
    required_fields = {"name", "price", "quantity", "category_name", "description"}

    if not data or not required_fields.issubset(data.keys()):
        return response(False, "Missing required fields", status_code=400)

    try:
        # Generate Product ID
        if "id" in data and data["id"].strip():
            product_id = data["id"]
        else:
            last_product = db.fetchone("SELECT id FROM products ORDER BY CAST(SUBSTR(id, 2) AS INTEGER) DESC LIMIT 1")
            last_number = int(last_product["id"][1:]) if last_product and last_product["id"] else 100000
            product_id = f"P{last_number + 1:06d}"

        # Add Product
        inventory.add_product(
            product_id=product_id,
            name=data["name"],
            price=float(data["price"]),
            quantity=int(data["quantity"]),
            category_name=data["category_name"],
            description=data["description"]
        )

        return response(True, "Product added successfully", {"product_id": product_id}, status_code=201)
    except Exception as e:
        logging.error(f"Error adding product: {str(e)}")
        return response(False, "Internal Server Error", status_code=500)


@app.route('/products/<string:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product details (price or quantity)"""
    data = request.json
    product = inventory.get_product(product_id)

    if not product:
        return response(False, "Product not found", status_code=404)

    update_fields = []
    update_values = []

    if "price" in data:
        update_fields.append("price = ?")
        update_values.append(float(data["price"]))
    if "quantity" in data:
        update_fields.append("quantity = ?")
        update_values.append(int(data["quantity"]))

    if not update_fields:
        return response(False, "No valid fields to update", status_code=400)

    update_query = f"UPDATE products SET {', '.join(update_fields)} WHERE id = ?"
    update_values.append(product_id)

    try:
        db.execute(update_query, tuple(update_values))
        return response(True, "Product updated successfully")
    except Exception as e:
        logging.error(f"Error updating product {product_id}: {str(e)}")
        return response(False, "Internal Server Error", status_code=500)


@app.route('/products/<string:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    product = inventory.get_product(product_id)
    if not product:
        return response(False, "Product not found", status_code=404)

    try:
        inventory.remove_product(product_id)
        return response(True, "Product deleted successfully")
    except Exception as e:
        logging.error(f"Error deleting product {product_id}: {str(e)}")
        return response(False, "Internal Server Error", status_code=500)


@app.route('/categories/<string:category_name>', methods=['DELETE'])
def delete_category(category_name):
    """Delete a category"""
    category = inventory.get_category(category_name)
    if not category:
        return response(False, "Category not found", status_code=404)

    try:
        inventory.remove_category(category_name)
        return response(True, "Category deleted successfully")
    except Exception as e:
        logging.error(f"Error deleting category {category_name}: {str(e)}")
        return response(False, "Internal Server Error", status_code=500)


if __name__ == '__main__':
    app.run(debug=True)
