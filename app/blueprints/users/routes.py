from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.models.models import User, Customer, db  # Ensure Customer is imported
from app.utils.util import encode_token, decode_token
from app.utils.decorator import role_required

# Blueprint for users module
users_bp = Blueprint('users', __name__)

# Login endpoint
@users_bp.route('/login', methods=['POST'])
def login():
    """
    Log in a user and return a JWT token.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Find user in the database
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # Extract roles from the user
        role_names = [role.role_name for role in user.roles]
        # Generate a JWT token
        auth_token = encode_token(user.id, role_names)
        resp = {
            "status": "success",
            "message": "Successfully logged in",
            "auth_token": auth_token
        }
        return jsonify(resp), 200
    else:
        # Invalid username or password
        resp = {
            "status": "fail",
            "message": "Invalid username or password"
        }
        return jsonify(resp), 401

# Get all customers endpoint (admin-only)
@users_bp.route('/api/customers', methods=['GET'])
@role_required(['admin'])  # Enforce access for admin role
def get_customers():
    """
    Retrieve all customers (admin-only).
    """
    try:
        # Fetch all customers from the database
        customers = Customer.query.all()
        return jsonify([
            {'id': cust.id, 'name': cust.name, 'email': cust.email, 'phone': cust.phone}
            for cust in customers
        ]), 200
    except Exception as e:
        # Handle potential database or query errors
        return jsonify({"message": f"Error retrieving customers: {str(e)}"}), 500

# Inspect token endpoint
@users_bp.route('/inspect-token', methods=['GET'])
def inspect_token():
    """
    Decode and inspect the JWT token provided in the Authorization header.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Token missing"}), 403

    token = auth_header.split(" ")[1]
    try:
        # Decode the token
        payload = decode_token(token)
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"message": f"Token invalid! {str(e)}"}), 401
