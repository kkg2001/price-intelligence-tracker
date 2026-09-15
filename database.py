import sqlite3

DB_FILE = "price_intelligence.db"

def get_connection():
    return sqlite3.connect(DB_FILE)


def get_product(product_id):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            product_id,
            product_name,
            brand,
            category,
            current_price
        FROM products
        WHERE product_id = ?
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    connection.close()

    if product is None:
        return None

    return {
        "product_id": product[0],
        "product_name": product[1],
        "brand": product[2],
        "category": product[3],
        "current_price": product[4],
    }


def get_price_history(product_id):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT date, price
        FROM price_history
        WHERE product_id = ?
        ORDER BY date
        """,
        (product_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "date": row[0],
            "price": row[1]
        }
        for row in rows
    ]


def get_all_products():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            product_id,
            product_name,
            brand,
            category,
            current_price
        FROM products
        ORDER BY product_name
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "product_id": row[0],
            "product_name": row[1],
            "brand": row[2],
            "category": row[3],
            "current_price": row[4],
        }
        for row in rows
    ]
