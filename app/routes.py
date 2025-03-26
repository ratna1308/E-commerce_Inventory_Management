from flask import Flask, request, jsonify
from models import Inventory, Database

app = Flask(__name__)

# Initialize database
db = Database()
inventory = Inventory(db)

@app.route('/products', methods=['GET'])
def get_all_products():
    products = inventory.get_all_products()
    return jsonify(products)

@app.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    product = inventory.get_product(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    required_fields = {"name", "price", "quantity", "category_name", "description"}

    if not data or not required_fields.issubset(data.keys()):
        return jsonify({"error": "Missing required fields"}), 400

    if "id" in data and data["id"].strip():
        product_id = data["id"]
    else:
        last_product = db.fetchone("SELECT id FROM products ORDER BY CAST(SUBSTR(id, 2) AS INTEGER) DESC LIMIT 1")

        if last_product and last_product["id"]:
            try:
                last_number = int(last_product["id"][1:])  
            except ValueError:
                last_number = 100000  
        else:
            last_number = 100000  

        product_id = f"P{last_number + 1:06d}" 

    inventory.add_product(
        product_id=product_id,
        name=data["name"],
        price=float(data["price"]),
        quantity=int(data["quantity"]),
        category_name=data["category_name"],
        description=data["description"]
    )

    return jsonify({"message": "Product added successfully!", "product_id": product_id}), 201


@app.route('/products/<string:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    product = inventory.get_product(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    update_query = "UPDATE products SET "
    update_fields = []
    update_values = []
    
    if "price" in data:
        update_fields.append("price = ?")
        update_values.append(float(data["price"]))
    if "quantity" in data:
        update_fields.append("quantity = ?")
        update_values.append(int(data["quantity"]))

    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    update_query += ", ".join(update_fields) + " WHERE id = ?"
    update_values.append(product_id)

    db.execute(update_query, tuple(update_values))
    return jsonify({"message": "Product updated successfully!"})

@app.route('/categories', methods=['GET'])  
def get_all_categories():
    categories = inventory.get_all_categories()
    return jsonify(categories)

@app.route('/categories/<string:category_name>', methods=['GET'])  
def get_category(category_name):
    category = inventory.get_category(category_name)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(category)

if __name__ == '__main__':
    app.run(debug=True)
