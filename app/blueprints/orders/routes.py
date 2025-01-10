# Updated orders.routes
from flask import Blueprint, jsonify, request
from app.models.models import Order, db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.models.models import Product


limiter = Limiter(get_remote_address)
orders_bp = Blueprint('orders', __name__)

# create an order (5 requests per minute)
@orders_bp.route('', methods=['POST'])
@limiter.limit("5 per minute")
def create_order():
    data = request.get_json()
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    total_price = product.price * data['quantity']
    new_order = Order(customer_id=data['customer_id'], product_id=data['product_id'], quantity=data['quantity'],
                      total_price=total_price)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

# get all orders with pagination (10 requests per minute)
@orders_bp.route('', methods=['GET'])
@limiter.limit("10 per minute")
def get_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    orders = Order.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'orders': [
            {
                'id': order.id,
                'customer_id': order.customer_id,
                'product_id': order.product_id,
                'quantity': order.quantity,
                'total_price': order.total_price
            }
            for order in orders.items
        ],
        'total': orders.total,
        'page': orders.page,
        'pages': orders.pages
    }), 200
