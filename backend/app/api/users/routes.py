from flask import Blueprint, request
from backend.app.utils.response import ok, bad_request, unauthorized, conflict
from backend.app.repositories.users import get_by_id, update_user, update_tag
from backend.app.services.auth import verify_token

bp = Blueprint("users", __name__, url_prefix="/users")

def _current_user_id():
    auth = request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        return None
    token = auth.split(" ", 1)[1]
    uid = verify_token(token)
    return uid

@bp.get("/me")
def me():
    uid = _current_user_id()
    if not uid:
        return unauthorized("missing or invalid token")
    user = get_by_id(uid)
    if not user:
        return unauthorized("user not found")
    return ok({k: user[k] for k in ["id", "phone", "nickname", "tag", "default_city_id", "role"]})

@bp.put("/me")
def update_me():
    uid = _current_user_id()
    if not uid:
        return unauthorized("missing or invalid token")
    data = request.get_json(silent=True) or {}
    nickname = data.get("nickname")
    phone = data.get("phone")
    default_city_id = data.get("default_city_id")
    user, err = update_user(uid, nickname=nickname, phone=phone, default_city_id=default_city_id)
    if err == "bad_request":
        return bad_request("no fields to update")
    if err == "conflict":
        return conflict("phone exists")
    return ok({k: user[k] for k in ["id", "phone", "nickname", "tag", "default_city_id", "role"]})

@bp.put("/me/tags")
def update_me_tags():
    uid = _current_user_id()
    if not uid:
        return unauthorized("missing or invalid token")
    data = request.get_json(silent=True) or {}
    tag = data.get("tag")
    user, err = update_tag(uid, tag)
    if err == "bad_request":
        return bad_request("invalid tag")
    return ok({k: user[k] for k in ["id", "phone", "nickname", "tag", "default_city_id", "role"]})
