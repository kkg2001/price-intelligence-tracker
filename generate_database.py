import os
import random
import sqlite3
from datetime import date, timedelta

import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATA_DIR = "data"
DB_FILE = "price_intelligence.db"

END_DATE = date.today()
DAYS = 180

random.seed(42)

os.makedirs(DATA_DIR, exist_ok=True)


# --------------------------------------------------
# 1. Product data
# --------------------------------------------------

products = [
    ("P001", "MacBook Air M4", "Apple", "Laptop", 89999),
    ("P002", "MacBook Pro M4", "Apple", "Laptop", 149999),
    ("P003", "ThinkPad E14", "Lenovo", "Laptop", 72999),
    ("P004", "Dell XPS 13", "Dell", "Laptop", 104999),

    ("P005", "Galaxy S25", "Samsung", "Smartphone", 74999),
    ("P006", "iPhone 17", "Apple", "Smartphone", 79999),
    ("P007", "Pixel 10", "Google", "Smartphone", 69999),
    ("P008", "OnePlus 14", "OnePlus", "Smartphone", 59999),

    ("P009", "Galaxy Tab S11", "Samsung", "Tablet", 64999),
    ("P010", "iPad Air M3", "Apple", "Tablet", 67999),

    ("P011", "Sony WH-1000XM6", "Sony", "Headphones", 29999),
    ("P012", "Bose QuietComfort Ultra", "Bose", "Headphones", 27999),

    ("P013", "AirPods Pro 3", "Apple", "Earbuds", 24999),
    ("P014", "Sony WF-1000XM6", "Sony", "Earbuds", 22999),

    ("P015", "Apple Watch Series 11", "Apple", "Smartwatch", 44999),
    ("P016", "Galaxy Watch 8", "Samsung", "Smartwatch", 34999),

    ("P017", "Kindle Paperwhite", "Amazon", "E-reader", 14999),
    ("P018", "GoPro Hero 14", "GoPro", "Camera", 44999),

    ("P019", "DJI Mini 5", "DJI", "Drone", 89999),
    ("P020", "Logitech MX Master 4", "Logitech", "Accessories", 9999),
]


products_df = pd.DataFrame(
    products,
    columns=[
        "product_id",
        "product_name",
        "brand",
        "category",
        "current_price",
    ],
)


products_df.to_csv(
    os.path.join(DATA_DIR, "products.csv"),
    index=False
)


# --------------------------------------------------
# 2. Generate price history
# --------------------------------------------------

START_DATE = END_DATE - timedelta(days=DAYS - 1)

history = []


for (
    product_id,
    product_name,
    brand,
    category,
    current_price
) in products:

    price = current_price * random.uniform(1.05, 1.18)

    volatility = random.uniform(0.003, 0.01)

    for day_number in range(DAYS):

        current_date = (
            START_DATE + timedelta(days=day_number)
        )

        movement = random.gauss(
            0,
            volatility
        )

        price = price * (1 + movement)

        minimum = current_price * 0.90
        maximum = current_price * 1.25

        price = max(
            minimum,
            min(price, maximum)
        )

        history.append(
            {
                "product_id": product_id,
                "date": current_date.isoformat(),
                "price": round(price / 100) * 100,
            }
        )


history_df = pd.DataFrame(history)


# Make latest price equal current price
for (
    product_id,
    _,
    _,
    _,
    current_price
) in products:

    history_df.loc[
        (
            history_df["product_id"] == product_id
        )
        &
        (
            history_df["date"] == END_DATE.isoformat()
        ),
        "price",
    ] = current_price


history_df.to_csv(
    os.path.join(DATA_DIR, "price_history.csv"),
    index=False
)


# --------------------------------------------------
# 3. Create SQLite database
# --------------------------------------------------

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)


connection = sqlite3.connect(DB_FILE)

cursor = connection.cursor()


cursor.execute("""
CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    brand TEXT NOT NULL,
    category TEXT NOT NULL,
    current_price REAL NOT NULL
)
""")


cursor.execute("""
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    date TEXT NOT NULL,
    price REAL NOT NULL,

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
)
""")


# Insert products
products_df.to_sql(
    "products",
    connection,
    if_exists="append",
    index=False,
)


# Insert price history
history_df.to_sql(
    "price_history",
    connection,
    if_exists="append",
    index=False,
)


# Index for faster queries
cursor.execute("""
CREATE INDEX idx_price_history_product_date
ON price_history(product_id, date)
""")


connection.commit()


# --------------------------------------------------
# 4. Verify database
# --------------------------------------------------

product_count = cursor.execute(
    "SELECT COUNT(*) FROM products"
).fetchone()[0]


history_count = cursor.execute(
    "SELECT COUNT(*) FROM price_history"
).fetchone()[0]


print("\nData generation completed!")
print(f"End date: {END_DATE}")
print(f"Products: {product_count}")
print(f"Price history records: {history_count}")

print("\nFiles created:")
print(
    os.path.join(DATA_DIR, "products.csv")
)
print(
    os.path.join(DATA_DIR, "price_history.csv")
)
print(DB_FILE)


connection.close()