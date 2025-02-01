import datetime

import jwt

from config import DevelopmentConfig

SECRET_KEY = DevelopmentConfig.SECRET_KEY


def encode_token(user_id, roles):
    """
    Generate a JWT token with user ID and roles as payload.
    """
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id,
            "roles": roles,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    except Exception as e:
        return str(e)


def decode_token(token):
    """
    Decode a JWT token to extract payload.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired.")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token.")
