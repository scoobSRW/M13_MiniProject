from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from app.models.models import Customer, User, db
from app.utils.decorator import role_required
from app.utils.util import decode_token, encode_token

# Blueprint for users module
users_bp = Blueprint("users", __name__)


# Login endpoint
@users_bp.route("/login", methods=["POST"])
def login():
    """
    Log in a user and return a JWT token.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        role_names = [role.role_name for role in user.roles]
        auth_token = encode_token(user.id, role_names)
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Successfully logged in",
                    "auth_token": auth_token,
                }
            ),
            200,
        )
    else:
        return (
            jsonify({"status": "fail", "message": "Invalid username or password"}),
            401,
        )


# Get all customers endpoint (admin-only)
@users_bp.route("/api/customers", methods=["GET"])
@role_required(["admin"])
def get_customers():
    """
    Retrieve all customers (admin-only).
    """
    try:
        customers = Customer.query.all()
        return (
            jsonify(
                [
                    {
                        "id": cust.id,
                        "name": cust.name,
                        "email": cust.email,
                        "phone": cust.phone,
                    }
                    for cust in customers
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"message": f"Error retrieving customers: {str(e)}"}), 500


# Inspect token endpoint
@users_bp.route("/inspect-token", methods=["GET"])
def inspect_token():
    """
    Decode and inspect the JWT token provided in the Authorization header.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"message": "Token missing"}), 403

    token = auth_header.split(" ")[1]
    try:
        payload = decode_token(token)
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"message": f"Token invalid! {str(e)}"}), 401


# Update user (admin-only)
@users_bp.route("/<int:user_id>", methods=["PUT"])
@role_required(["admin"])
def update_user(user_id):
    """
    Update user information (admin-only).
    """
    data = request.get_json()
    user = User.query.get_or_404(user_id)

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)

    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200


# Delete user (admin-only)
@users_bp.route("/<int:user_id>", methods=["DELETE"])
@role_required(["admin"])
def delete_user(user_id):
    """
    Delete a user (admin-only).
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
