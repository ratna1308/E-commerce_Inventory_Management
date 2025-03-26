import pytest
from models import Database, Inventory

@pytest.fixture
def db():
    """Creates a test database instance."""
    test_db = Database(db_name=":memory:") 
    return test_db

@pytest.fixture
def inventory(db):
    """Creates an Inventory instance using the test database."""
    return Inventory(db)

# ==== CATEGORY TESTS ====

def test_add_category(inventory):
    inventory.add_category("Electronics", "Gadgets and devices")
    category = inventory.db.fetchone("SELECT * FROM categories WHERE name = ?", ("Electronics",))
    assert category is not None
    assert category[1] == "Electronics"
    assert category[2] == "Gadgets and devices"

# ==== PRODUCT TESTS ====

def test_add_product(inventory):
    inventory.add_product("P001", "Laptop", 1500.0, "Electronics", "Gadgets and devices", 10)
    product = inventory.db.fetchone("SELECT * FROM products WHERE id = ?", ("P001",))
    assert product is not None
    assert product[1] == "Laptop"
    assert product[2] == 1500.0
    assert product[3] == 10


def test_get_product(inventory):
    inventory.add_product("P002", "Smartphone", 800.0, "Electronics", "Gadgets and devices", 25)
    product = inventory.get_product("P002")
    assert product is not None
    assert product["Name"] == "Smartphone"
    assert product["Price"] == 800.0
    assert product["Quantity"] == 25


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
    assert products[0]["Name"] == "TV"
    assert products[1]["Name"] == "Microwave"


def test_update_product(inventory):
    inventory.add_product("P006", "Headphones", 100.0, "Accessories", "Audio devices", 30)
    inventory.db.execute("UPDATE products SET price = ?, quantity = ? WHERE id = ?", (120.0, 25, "P006"))
    product = inventory.get_product("P006")
    assert product["Price"] == 120.0
    assert product["Quantity"] == 25

if __name__ == "__main__":
    pytest.main()

