# Updated products.routes
from flask import Blueprint, jsonify, request
from app.models.models import Product, db
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(get_remote_address)
products_bp = Blueprint('products', __name__)

# create a product (5 requests per minute)
@products_bp.route('', methods=['POST'])
@limiter.limit("5 per minute")
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

# get all products with pagination (10 requests per minute)
@products_bp.route('', methods=['GET'])
@limiter.limit("10 per minute")
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'products': [
            {
                'id': prod.id,
                'name': prod.name,
                'price': prod.price
            }
            for prod in products.items
        ],
        'total': products.total,
        'page': products.page,
        'pages': products.pages
    }), 200
