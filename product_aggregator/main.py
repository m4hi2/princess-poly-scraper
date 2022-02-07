import os
from unicodedata import name

import psycopg2

import bus

product_queue = "products"

product_insert_query = """INSERT INTO 
                        product(name, price, full_price, size, color, image_links, stock, description)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

db_host = os.getenv("PGHOST", "127.0.0.1")
db_user = os.getenv("PGUSER", "postgres")
db_pass = os.getenv("PGPASS", "postgres")
db_name = os.getenv("PGDB", "postgres")
db_port = os.getenv("PGPORT", "5432")
def main():

    bus.declare([product_queue])
    conn = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5438", database="postgres")
    cur = conn.cursor()
    def callback(ch, method, properties, product):
        products_to_insert = (
            product.name,
            product.price,
            product.full_price,
            product.size,
            product.color,
            product.image_links,
            product.stock,
            product.description
        )
        cur.execute(product_insert_query, products_to_insert)
        conn.commit()
    bus.consume(product_queue, callback)
    bus.loop()
    
    
if __name__ == "__main__":
    main()
    