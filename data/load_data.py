import csv
import sqlite3
from cerberus import Validator
from data.data_schemas import *

def load_csv(csv_file, csv_schema):
    """
    Load and validate data from CSV
    """
    with open(csv_file, newline='') as cf:
        v = Validator(csv_schema, purge_unknown=True)
        reader = csv.DictReader(cf)
        values = [v.document for x in reader if v.validate(x)]
    return values

# The database ceases to exist as soon as the database connection is closed.
con = sqlite3.connect(":memory:", check_same_thread=False)
cur = con.cursor()

cur.executescript("""
CREATE TABLE orders(
    id INTEGER NOT NULL PRIMARY KEY,
    created_at TEXT NOT NULL,
    vendor_id INTEGER NOT NULL,
    CUSTOMER_id INTEGER NOT NULL
);

CREATE TABLE order_lines(
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    product_description TEXT,
    product_price INTEGER NOT NULL,
    product_vat_rate REAL NOT NULL,
    discount_rate REAL NOT NULL,
    quantity INTEGER NOT NULL,
    full_price_amount INTEGER NOT NULL,
    discounted_amount REAL NOT NULL,
    vat_amount REAL NOT NULL,
    total_amount REAL NOT NULL
);

CREATE TABLE products(
    id INTEGER NOT NULL PRIMARY KEY,
    description TEXT
);

CREATE TABLE promotions(
    id INTEGER NOT NULL PRIMARY KEY,
    description TEXT
);

CREATE TABLE product_promotions(
    date TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    promotion_id INTEGER NOT NULL
);

CREATE TABLE vendor_commissions(
    date TEXT NOT NULL,
    vendor_id INTEGER NOT NULL,
    rate REAL NOT NULL
);

""")

orders = load_csv("data/orders.csv", order_schema)
cur.executemany(
    "INSERT INTO orders VALUES (?,?,?,?)",
    [
        (
            i['id'], i['created_at'], i['vendor_id'], i['customer_id']
        )
        for i in orders
    ]
)

order_lines = load_csv("data/order_lines.csv", order_line_schema)
cur.executemany(
    "INSERT INTO order_lines VALUES (?,?,?,?,?,?,?,?,?,?,?)",
    [
        (
            i[ 'order_id' ],
            i[ 'product_id' ],
            i[ 'product_description' ],
            i[ 'product_price' ],
            i[ 'product_vat_rate' ],
            i[ 'discount_rate' ],
            i[ 'quantity' ],
            i[ 'full_price_amount' ],
            i[ 'discounted_amount' ],
            i[ 'vat_amount' ],
            i[ 'total_amount' ]
        )
        for i in order_lines
    ]
)

products = load_csv("data/products.csv", product_schema)
cur.executemany(
    "INSERT INTO products VALUES (?,?)",
    [ (i['id'], i['description']) for i in products]
)

promotions = load_csv("data/promotions.csv", promotion_schema)
cur.executemany(
    "INSERT INTO promotions VALUES (?,?)",
    [ (i['id'], i['description']) for i in promotions]
)

product_promotions = load_csv("data/product_promotions.csv", product_promotion_schema)
cur.executemany(
    "INSERT INTO product_promotions VALUES (?,?,?)",
    [
        (i['date'], i['product_id'], i['promotion_id'])
        for i in product_promotions
    ]
)

vendor_commissions = load_csv("data/commissions.csv", vendor_commissions_schema)
cur.executemany(
    "INSERT INTO vendor_commissions VALUES (?,?,?)",
    [
        (i['date'], i['vendor_id'], i['rate'])
        for i in vendor_commissions
    ]
)
