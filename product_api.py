from flask import Blueprint, request, jsonify
from database_config import get_db_connection

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO product (name, price, category) VALUES (%s, %s, %s) RETURNING id",
                (data['name'], data['price'], data['category']))
    product_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'product_id': product_id}), 201

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM product WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    if product:
        return jsonify({'id': product[0], 'name': product[1], 'price': product[2], 'category': product[3]})
    return jsonify({'error': 'Product not found'}), 404

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE product SET name = %s, price = %s, category = %s WHERE id = %s",
                (data['name'], data['price'], data['category'], product_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Product updated'})

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM product WHERE id = %s", (product_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Product deleted'})
