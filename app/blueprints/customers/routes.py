from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.blueprints.services.customerservice import (create_customer,
                                                     delete_customer,
                                                     update_customer)
from app.models.models import Customer

customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/<int:customer_id>", methods=["GET"])
@jwt_required()
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    return (
        jsonify(
            {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
            }
        ),
        200,
    )


@customers_bp.route("", methods=["POST"])
@jwt_required()
def add_customer():
    data = request.get_json()
    customer = create_customer(data)
    return jsonify({"id": customer.id, "name": customer.name}), 201


@customers_bp.route("/<int:customer_id>", methods=["PUT"])
@jwt_required()
def modify_customer(customer_id):
    data = request.get_json()
    customer = update_customer(customer_id, data)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    return (
        jsonify(
            {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
            }
        ),
        200,
    )


@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
@jwt_required()
def remove_customer(customer_id):
    customer = delete_customer(customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    return jsonify({"message": "Customer deleted successfully"}), 200
