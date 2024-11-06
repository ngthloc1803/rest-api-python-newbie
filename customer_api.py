from flask import Blueprint, jsonify, request

from database_config import get_db_connection

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO customer (name, phone, email, address) VALUES (%s, %s, %s, %s) RETURNING customer_id",
                (data['name'], data['phone'], data['email'], data['address']))
    customer_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'customer_id': customer_id}), 201

@customer_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customer WHERE customer_id = %s", (customer_id,))
    customer = cur.fetchone()
    cur.close()
    conn.close()
    if customer:
        return jsonify({'customer_id': customer[0], 'name': customer[1], 'phone': customer[2], 'email': customer[3], 'address': customer[4]})
    return jsonify({'error': 'Customer not found'}), 404

@customer_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE customer SET name = %s, phone = %s, email = %s, address = %s WHERE customer_id = %s",
                (data['name'], data['phone'], data['email'], data['address'], customer_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Customer updated'})

@customer_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM customer WHERE customer_id = %s", (customer_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Customer deleted'})

@customer_bp.route('/customers/get-all', methods=['GET'])
def get_all_customers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customer")
    customers = cur.fetchall()
    cur.close()
    conn.close()

    if customers:
        all_customers = []
        for customer in customers:
            all_customers.append({
                'customer_id': customer[0],
                'name': customer[1],
                'phone': customer[2],
                'email': customer[3],
                'address': customer[4]
            })
        return jsonify(all_customers)
    else:
        return jsonify({'message': 'No customers found'}), 404
