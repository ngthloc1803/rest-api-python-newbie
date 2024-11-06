import psycopg2
from psycopg2 import sql

#cấu hình thông tin kết nối đến PostgreSQL
DB_HOST = "localhost"
DB_NAME = "customer"
DB_USER = "postgres"
DB_PASS = "123456"

#kết nối đến cơ sở dữ liệu
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

#tạo bảng nếu chưa tồn tại
def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    
    #tạo bảng Customer
    cur.execute('''
        CREATE TABLE IF NOT EXISTS customer (
            customer_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(15),
            email VARCHAR(100) UNIQUE,
            address VARCHAR(255)
        )
    ''')
    
    #tạo bảng Product
    cur.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price FLOAT NOT NULL,
            category VARCHAR(50)
        )
    ''')
    
    #tạo bảng Orders
    cur.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES customer(customer_id),
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    #tạo bảng Order_Detail
    cur.execute('''
        CREATE TABLE IF NOT EXISTS order_detail (
            id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(order_id),
            product_id INTEGER REFERENCES product(id),
            quantity INTEGER NOT NULL,
            price FLOAT NOT NULL
        )
    ''')

    #confirm changes + close
    conn.commit()
    cur.close()
    conn.close()

create_tables()
