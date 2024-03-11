import sqlite3

class InventoryDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create inventory table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                            id INTEGER PRIMARY KEY,
                            item_name TEXT NOT NULL,
                            quantity INTEGER NOT NULL,
                            purchase_price REAL NOT NULL,
                            selling_price REAL NOT NULL
                        )''')
        self.conn.commit()

        # Create customers table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                            id INTEGER PRIMARY KEY,
                            item_id INTEGER NOT NULL,
                            customer_name TEXT NOT NULL,
                            booking_date TEXT NOT NULL,
                            location TEXT NOT NULL,
                            warranty_type TEXT,
                            quantity INTEGER NOT NULL,
                            rental_price REAL NOT NULL,
                            total_price REAL NOT NULL,
                            delivery_service BOOLEAN NOT NULL,
                            phone_number TEXT,
                            FOREIGN KEY(item_id) REFERENCES inventory(id)
                        )''')

    def add_item(self, item_name, quantity, purchase_price, selling_price):
        self.cursor.execute("INSERT INTO inventory (item_name, quantity, purchase_price, selling_price) VALUES (?, ?, ?, ?)",
                            (item_name, quantity, purchase_price, selling_price))
        self.conn.commit()

    def edit_item(self, item_id, item_name, quantity, purchase_price, selling_price):
        self.cursor.execute("UPDATE inventory SET item_name=?, quantity=?, purchase_price=?, selling_price=? WHERE id=?",
                            (item_name, quantity, purchase_price, selling_price, item_id))
        self.conn.commit()

    def delete_item(self, item_id):
        self.cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        self.conn.commit()

    def get_all_items(self):
        self.cursor.execute("SELECT * FROM inventory")
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()
