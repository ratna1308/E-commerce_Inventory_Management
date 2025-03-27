import sqlite3
from typing import List

class Database:
    def __init__(self, db_name="inventory.db"):
        self.db_name = db_name  
        self.create_tables()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row  
        return conn

    def create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, description TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS products (id TEXT PRIMARY KEY, name TEXT NOT NULL, price REAL NOT NULL, quantity INTEGER NOT NULL, category_id INTEGER, FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE)")
            conn.commit()

    def execute(self, query: str, params=()):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def fetchall(self, query: str, params=()) -> List[dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def fetchone(self, query: str, params=()) -> dict:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None


class Inventory:
    def __init__(self, db: Database):
        self.db = db

    def add_category(self, category_name: str, description: str):
        self.db.execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", (category_name, description))

    def add_product(self, product_id: str, name: str, price: float, category_name: str, description: str, quantity: int):
        self.add_category(category_name, description)
        category = self.db.fetchone("SELECT id FROM categories WHERE name = ?", (category_name,))
        if category:
            self.db.execute("INSERT INTO products (id, name, price, quantity, category_id) VALUES (?, ?, ?, ?, ?)", (product_id, name, price, quantity, category["id"]))

    def remove_product(self, product_id: str):
        self.db.execute("DELETE FROM products WHERE id = ?", (product_id,))

    def get_product(self, product_id: str):
        return self.db.fetchone("SELECT p.id, p.name, p.price, p.quantity, c.name as category FROM products p LEFT JOIN categories c ON p.category_id = c.id WHERE p.id = ?", (product_id,))

    def get_all_products(self):
        return self.db.fetchall("SELECT p.id, p.name, p.price, p.quantity, c.name as category FROM products p LEFT JOIN categories c ON p.category_id = c.id")

    def get_products_by_category(self, category_name: str):
        category = self.db.fetchone("SELECT id FROM categories WHERE name = ?", (category_name,))
        if category:
            return self.db.fetchall("SELECT id, name, price, quantity FROM products WHERE category_id = ?", (category["id"],))
        return []

    def get_category(self, category_name: str):
        return self.db.fetchone("SELECT * FROM categories WHERE name = ?", (category_name,))

    def get_all_categories(self):
        return self.db.fetchall("SELECT * FROM categories")

    def __str__(self):
        total_products = self.db.fetchone('SELECT COUNT(*) as count FROM products')["count"]
        total_categories = self.db.fetchone('SELECT COUNT(*) as count FROM categories')["count"]
        return f"Inventory with {total_products} products and {total_categories} categories."
