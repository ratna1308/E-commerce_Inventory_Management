import pytest
from app.models import Database, Inventory

@pytest.fixture
def db():
    """Creates a test database instance."""
    test_db = Database(db_name=":inventory.db:")  
    return test_db

@pytest.fixture
def inventory(db):
    """Creates an Inventory instance using the test database and clears existing data."""
    inventory = Inventory(db)
    
    # Clear existing data before each test
    with inventory.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products")  # Clear products table
        cursor.execute("DELETE FROM categories")  # Clear categories table
        conn.commit()
    
    return inventory

# ==== CATEGORY TESTS ====

def test_add_category(inventory):
    inventory.add_category("Electronics", "Gadgets and devices")
    category = inventory.db.fetchone("SELECT * FROM categories WHERE name = ?", ("Electronics",))
    assert category is not None
    assert category["name"] == "Electronics"
    assert category["description"] == "Gadgets and devices"

def test_get_category(inventory):
    inventory.add_category("Appliances", "Home appliances")
    category = inventory.get_category("Appliances")
    assert category is not None
    assert category["name"] == "Appliances"
    assert category["description"] == "Home appliances"

def test_get_all_categories(inventory):
    inventory.add_category("Books", "Educational materials")
    inventory.add_category("Furniture", "Home furniture")
    categories = inventory.get_all_categories()
    assert len(categories) == 2
    assert categories[0]["name"] == "Books"
    assert categories[1]["name"] == "Furniture"

# ==== PRODUCT TESTS ====

def test_add_product(inventory):
    inventory.add_product("P001", "Laptop", 1500.0, "Electronics", "Gadgets and devices", 10)
    product = inventory.db.fetchone("SELECT * FROM products WHERE id = ?", ("P001",))
    assert product is not None
    assert product["name"] == "Laptop"
    assert product["price"] == 1500.0
    assert product["quantity"] == 10

def test_get_product(inventory):
    inventory.add_product("P002", "Smartphone", 800.0, "Electronics", "Gadgets and devices", 25)
    product = inventory.get_product("P002")
    assert product is not None
    assert product["name"] == "Smartphone"
    assert product["price"] == 800.0
    assert product["quantity"] == 25

def test_remove_product(inventory):
    inventory.add_product("P003", "Tablet", 500.0, "Electronics", "Gadgets", 15)
    inventory.remove_product("P003")
    product = inventory.get_product("P003")
    assert product is None

def test_get_all_products(inventory):
    inventory.add_product("P004", "TV", 1000.0, "Appliances", "Home appliances", 5)
    inventory.add_product("P005", "Microwave", 200.0, "Appliances", "Kitchen appliances", 8)
    products = inventory.get_all_products()
    assert len(products) == 2
    assert products[0]["name"] == "TV"
    assert products[1]["name"] == "Microwave"

def test_get_products_by_category(inventory):
    inventory.add_product("P006", "Blender", 50.0, "Kitchen", "Kitchen appliances", 20)
    products = inventory.get_products_by_category("Kitchen")
    assert len(products) == 1
    assert products[0]["name"] == "Blender"

def test_update_product(inventory):
    inventory.add_product("P007", "Headphones", 100.0, "Accessories", "Audio devices", 30)
    inventory.db.execute("UPDATE products SET price = ?, quantity = ? WHERE id = ?", (120.0, 25, "P007"))
    product = inventory.get_product("P007")
    assert product["price"] == 120.0
    assert product["quantity"] == 25

if __name__ == "__main__":
    pytest.main()
