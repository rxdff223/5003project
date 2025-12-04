import os
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

def _serializer():
    secret = os.getenv("SECRET_KEY", "dev-secret")
    return URLSafeTimedSerializer(secret_key=secret, salt="auth-token")

def issue_token(user_id):
    s = _serializer()
    return s.dumps({"uid": user_id})

def verify_token(token, max_age=604800):
    s = _serializer()
    try:
        data = s.loads(token, max_age=max_age)
        return data.get("uid")
    except (BadSignature, SignatureExpired):
        return None
