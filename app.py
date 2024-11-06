from flask import Flask
from customer_api import customer_bp
from product_api import product_bp
from order_api import order_bp
from order_detail_api import order_detail_bp
from database_config import create_tables

app = Flask(__name__)

#create tables if not exist in database
create_tables()

#register blueprint
app.register_blueprint(customer_bp)
app.register_blueprint(product_bp)
app.register_blueprint(order_bp)
app.register_blueprint(order_detail_bp)

if __name__ == '__main__':
    app.run(debug=True)
