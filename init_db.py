import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# --- Create the Users Table (No changes) ---
print("Checking 'users' table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        moss_coins REAL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# --- Create the Vendors Table (No changes) ---
print("Checking 'vendors' table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_name TEXT NOT NULL,
        contact_name TEXT NOT NULL,
        mobile_number TEXT NOT NULL,
        udyam_id TEXT NOT NULL UNIQUE,
        business_address TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        cert_filename TEXT,
        profile_logo TEXT,
        cover_photo TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# --- NEW: Create the Items Table ---
# This table will store all products/items listed by vendors.
print("Creating 'items' table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL,
        unit TEXT, -- e.g., 'kg', 'pc', 'litre'
        stock_status TEXT DEFAULT 'In Stock',
        image_filename TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vendor_id) REFERENCES vendors (id)
    )
''')
print("'items' table created successfully.")


connection.commit()
connection.close()

print("\nDatabase 'database.db' has been updated successfully!")