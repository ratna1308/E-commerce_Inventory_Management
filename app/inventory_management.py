import tkinter as tk
from tkinter import ttk, messagebox
from models import Inventory, Database

class InventoryGUI:
    def __init__(self, root, inventory: Inventory):
        self.inventory = inventory
        self.root = root
        self.root.title("Inventory Management")
        self.root.geometry("500x500")
        
        self.create_main_menu()

    def create_main_menu(self):
        """Creates the main menu with navigation buttons."""
        tk.Label(self.root, text="Inventory Management System", font=("Arial", 16, "bold")).pack(pady=10)
        
        tk.Button(self.root, text="Manage Categories", font=("Arial", 12), command=self.open_category_form).pack(pady=5)
        tk.Button(self.root, text="Manage Products", font=("Arial", 12), command=self.open_product_form).pack(pady=5)
        tk.Button(self.root, text="Exit", font=("Arial", 12), command=self.root.quit).pack(pady=10)

    def open_category_form(self):
        """Opens the category management form."""
        CategoryForm(self.root, self.inventory)
    
    def open_product_form(self):
        """Opens the product management form."""
        ProductForm(self.root, self.inventory)

class CategoryForm:
    def __init__(self, root, inventory: Inventory):
        self.inventory = inventory
        self.window = tk.Toplevel(root)
        self.window.title("Manage Categories")
        self.window.geometry("400x300")

        tk.Label(self.window, text="Category Name", font=("Arial", 12)).pack()
        self.category_name = tk.Entry(self.window, font=("Arial", 12))
        self.category_name.pack(pady=5)
        
        tk.Label(self.window, text="Description", font=("Arial", 12)).pack()
        self.category_desc = tk.Entry(self.window, font=("Arial", 12))
        self.category_desc.pack(pady=5)
        
        tk.Button(self.window, text="Add Category", command=self.add_category).pack(pady=5)
        tk.Button(self.window, text="View Categories", command=self.list_categories).pack(pady=5)
    
    def add_category(self):
        try:
            name = self.category_name.get().strip()
            desc = self.category_desc.get().strip()

            if not name:
                messagebox.showerror("Input Error", "Category Name is required!")
                return

            self.inventory.add_category(name, desc)
            messagebox.showinfo("Success", "Category added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def list_categories(self):
        try:
            categories = self.inventory.db.fetchall("SELECT id, name FROM categories")
            if not categories:
                messagebox.showinfo("Categories", "No categories available.")
                return
            
            category_list = "\n".join([f"{cat['id']} - {cat['name']}" for cat in categories])
            messagebox.showinfo("Categories", category_list)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve categories: {str(e)}")

class ProductForm:
    def __init__(self, root, inventory: Inventory):
        self.inventory = inventory
        self.window = tk.Toplevel(root)
        self.window.title("Manage Products")
        self.window.geometry("400x400")
        
        tk.Label(self.window, text="Product Name", font=("Arial", 12)).pack()
        self.product_name = tk.Entry(self.window, font=("Arial", 12))
        self.product_name.pack(pady=5)
        
        tk.Label(self.window, text="Price", font=("Arial", 12)).pack()
        self.price = tk.Entry(self.window, font=("Arial", 12))
        self.price.pack(pady=5)
        
        tk.Label(self.window, text="Quantity", font=("Arial", 12)).pack()
        self.quantity = tk.Entry(self.window, font=("Arial", 12))
        self.quantity.pack(pady=5)
        
        tk.Label(self.window, text="Category", font=("Arial", 12)).pack()
        self.category_dropdown = ttk.Combobox(self.window, font=("Arial", 12))
        self.category_dropdown.pack(pady=5)
        self.load_categories()
        
        tk.Button(self.window, text="Add Product", command=self.add_product).pack(pady=5)
        tk.Button(self.window, text="View Products", command=self.list_products).pack(pady=5)

    def load_categories(self):
        try:
            categories = self.inventory.db.fetchall("SELECT name FROM categories")
            self.category_dropdown['values'] = [cat['name'] for cat in categories]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load categories: {str(e)}")

    def add_product(self):
        try:
            name = self.product_name.get().strip()
            price_input = self.price.get().strip()
            quantity_input = self.quantity.get().strip()
            category_name = self.category_dropdown.get().strip()

            if not name or not price_input or not quantity_input or not category_name:
                messagebox.showerror("Input Error", "All fields are required!")
                return
            
            try:
                price = float(price_input)
                quantity = int(quantity_input)
            except ValueError:
                messagebox.showerror("Input Error", "Price must be a number and Quantity must be an integer!")
                return

            category_desc = ""

            last_product = self.inventory.db.fetchone("SELECT id FROM products ORDER BY CAST(SUBSTR(id, 2) AS INTEGER) DESC LIMIT 1")
            if last_product and last_product["id"]:
                try:
                    last_number = int(last_product["id"][1:])
                except ValueError:
                    last_number = 100000  
            else:
                last_number = 100000  

            product_id = f"P{last_number + 1:06d}"

            self.inventory.add_product(product_id, name, price, category_name, category_desc, quantity)
            messagebox.showinfo("Success", "Product added successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def list_products(self):
        try:
            products = self.inventory.get_all_products()
            if not products:
                messagebox.showinfo("Products", "No products available.")
                return

            product_list = "\n".join(
                f"ID: {p['id']} | Name: {p['name']} | Price: {p['price']}₹ | Qty: {p['quantity']}"
                for p in products
            )
            messagebox.showinfo("Products", product_list)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve products: {str(e)}")

if __name__ == "__main__":
    try:
        db = Database()
        inventory = Inventory(db)
        root = tk.Tk()
        app = InventoryGUI(root, inventory)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start: {str(e)}")
