from flask import Blueprint, request, jsonify
from database_config import get_db_connection

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (customer_id) VALUES (%s) RETURNING order_id", (data['customer_id'],))
    order_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'order_id': order_id}), 201

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
    order = cur.fetchone()
    cur.close()
    conn.close()
    if order:
        return jsonify({'order_id': order[0], 'customer_id': order[1], 'order_date': order[2]})
    return jsonify({'error': 'Order not found'}), 404

@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Order deleted'})
