from functools import wraps

from flask import jsonify, request

from app.utils.util import decode_token


def role_required(required_roles):
    """
    Decorator to enforce role-based access control.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"message": "Token is missing!"}), 403

            try:
                token = auth_header.split(" ")[1]
                payload = decode_token(token)
                user_roles = payload.get("roles", [])
                if not any(role in required_roles for role in user_roles):
                    return (
                        jsonify(
                            {"message": "Access denied. Insufficient role permissions."}
                        ),
                        403,
                    )
            except Exception as e:
                return jsonify({"message": f"Token is invalid! {str(e)}"}), 401

            return func(*args, **kwargs)

        return wrapper

    return decorator
