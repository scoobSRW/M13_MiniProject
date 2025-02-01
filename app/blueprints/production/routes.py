from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.models.models import Order, Product, Production, db

limiter = Limiter(get_remote_address)
orders_bp = Blueprint("orders", __name__)
production_bp = Blueprint("production", __name__)


# create an order (5 requests per minute)
@orders_bp.route("", methods=["POST"])
@limiter.limit("5 per minute")
def create_order():
    data = request.get_json()
    product = Product.query.get(data["product_id"])
    if not product:
        return jsonify({"error": "Product not found"}), 404

    total_price = product.price * data["quantity"]
    new_order = Order(
        customer_id=data["customer_id"],
        product_id=data["product_id"],
        quantity=data["quantity"],
        total_price=total_price,
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order created successfully"}), 201


# get all orders with pagination (10 requests per minute)
@orders_bp.route("", methods=["GET"])
@limiter.limit("10 per minute")
def get_orders():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    orders = Order.query.paginate(page=page, per_page=per_page, error_out=False)
    return (
        jsonify(
            {
                "orders": [
                    {
                        "id": order.id,
                        "customer_id": order.customer_id,
                        "product_id": order.product_id,
                        "quantity": order.quantity,
                        "total_price": order.total_price,
                    }
                    for order in orders.items
                ],
                "total": orders.total,
                "page": orders.page,
                "pages": orders.pages,
            }
        ),
        200,
    )


# update an order (5 requests per minute)
@orders_bp.route("/<int:order_id>", methods=["PUT"])
@limiter.limit("5 per minute")
def update_order(order_id):
    data = request.get_json()
    order = Order.query.get_or_404(order_id)
    if "product_id" in data:
        product = Product.query.get(data["product_id"])
        if not product:
            return jsonify({"error": "Product not found"}), 404
        order.product_id = data["product_id"]
        order.total_price = product.price * order.quantity
    if "quantity" in data:
        order.quantity = data["quantity"]
        order.total_price = order.total_price / order.quantity * data["quantity"]
    db.session.commit()
    return jsonify({"message": "Order updated successfully"}), 200


# delete an order (5 requests per minute)
@orders_bp.route("/<int:order_id>", methods=["DELETE"])
@limiter.limit("5 per minute")
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully"}), 200


# record a production entry (5 requests per minute)
@production_bp.route("", methods=["POST"])
@limiter.limit("5 per minute")
def record_production():
    data = request.get_json()
    new_production = Production(
        product_id=data["product_id"],
        quantity_produced=data["quantity_produced"],
        date_produced=data["date_produced"],
    )
    db.session.add(new_production)
    db.session.commit()
    return jsonify({"message": "Production recorded successfully"}), 201


# get all production records (10 requests per minute)
@production_bp.route("", methods=["GET"])
@limiter.limit("10 per minute")
def get_production():
    production_records = Production.query.all()
    return (
        jsonify(
            [
                {
                    "id": record.id,
                    "product_id": record.product_id,
                    "quantity_produced": record.quantity_produced,
                    "date_produced": record.date_produced.isoformat(),
                }
                for record in production_records
            ]
        ),
        200,
    )


# update a production record (5 requests per minute)
@production_bp.route("/<int:production_id>", methods=["PUT"])
@limiter.limit("5 per minute")
def update_production(production_id):
    data = request.get_json()
    production = Production.query.get_or_404(production_id)
    production.product_id = data.get("product_id", production.product_id)
    production.quantity_produced = data.get(
        "quantity_produced", production.quantity_produced
    )
    production.date_produced = data.get("date_produced", production.date_produced)
    db.session.commit()
    return jsonify({"message": "Production record updated successfully"}), 200


# delete a production record (5 requests per minute)
@production_bp.route("/<int:production_id>", methods=["DELETE"])
@limiter.limit("5 per minute")
def delete_production(production_id):
    production = Production.query.get_or_404(production_id)
    db.session.delete(production)
    db.session.commit()
    return jsonify({"message": "Production record deleted successfully"}), 200
