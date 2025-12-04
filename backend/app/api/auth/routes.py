from flask import Blueprint, request
from backend.app.utils.response import ok, bad_request, unauthorized, conflict
from backend.app.repositories.users import get_by_phone, create, verify_password, get_by_id
from backend.app.services.auth import issue_token, verify_token

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    phone = data.get("phone")
    password = data.get("password")
    nickname = data.get("nickname")
    if not phone or not password:
        return bad_request("phone and password required")
    user, err = create(phone, password, nickname)
    if err == "exists":
        return conflict("phone exists")
    token = issue_token(user["id"])
    return ok({"user": {k: user[k] for k in ["id", "phone", "nickname", "tag", "default_city_id", "role"]}, "token": token})

@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    phone = data.get("phone")
    password = data.get("password")
    if not phone or not password:
        return bad_request("phone and password required")
    user = get_by_phone(phone)
    if not user or not verify_password(user, password):
        return unauthorized("invalid credentials")
    token = issue_token(user["id"])
    return ok({"token": token, "user": {k: user[k] for k in ["id", "phone", "nickname", "tag", "default_city_id", "role"]}})

@bp.get("/me")
def me():
    auth = request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        return unauthorized("missing token")
    token = auth.split(" ", 1)[1]
    uid = verify_token(token)
    if not uid:
        return unauthorized("invalid token")
    user = get_by_id(uid)
    if not user:
        return unauthorized("user not found")
    return ok({k: user[k] for k in ["id", "phone", "nickname", "tag", "default_city_id", "role"]})
