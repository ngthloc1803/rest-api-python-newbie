from flask import Blueprint, request, jsonify
from database_config import get_db_connection

order_detail_bp = Blueprint('order_detail_bp', __name__)

@order_detail_bp.route('/order_details', methods=['POST'])
def create_order_detail():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO order_detail (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s) RETURNING id",
                (data['order_id'], data['product_id'], data['quantity'], data['price']))
    order_detail_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'order_detail_id': order_detail_id}), 201

@order_detail_bp.route('/order_details/<int:order_detail_id>', methods=['GET'])
def get_order_detail(order_detail_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM order_detail WHERE id = %s", (order_detail_id,))
    order_detail = cur.fetchone()
    cur.close()
    conn.close()
    if order_detail:
        return jsonify({'id': order_detail[0], 'order_id': order_detail[1], 'product_id': order_detail[2], 'quantity': order_detail[3], 'price': order_detail[4]})
    return jsonify({'error': 'Order Detail not found'}), 404

@order_detail_bp.route('/order_details/<int:order_detail_id>', methods=['DELETE'])
def delete_order_detail(order_detail_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM order_detail WHERE id = %s", (order_detail_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Order Detail deleted'})
