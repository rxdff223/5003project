from backend.app.extensions.db import get_conn, put_conn
from werkzeug.security import generate_password_hash, check_password_hash

def get_by_phone(phone):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, phone, password_hash, nickname, default_city_id, tag, role FROM users WHERE phone=%s", (phone,))
        row = cur.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "phone": row[1],
            "password_hash": row[2],
            "nickname": row[3],
            "default_city_id": row[4],
            "tag": row[5],
            "role": row[6],
        }
    finally:
        put_conn(conn)

def get_by_id(user_id):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, phone, nickname, default_city_id, tag, role FROM users WHERE id=%s", (user_id,))
        row = cur.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "phone": row[1],
            "nickname": row[2],
            "default_city_id": row[3],
            "tag": row[4],
            "role": row[5],
        }
    finally:
        put_conn(conn)

def create(phone, password, nickname=None):
    existing = get_by_phone(phone)
    if existing:
        return None, "exists"
    ph = generate_password_hash(password)
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users(phone, password_hash, nickname) VALUES (%s, %s, %s) RETURNING id",
            (phone, ph, nickname),
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return get_by_id(new_id), None
    finally:
        put_conn(conn)

def verify_password(user, password):
    return check_password_hash(user["password_hash"], password)

def phone_exists(phone, exclude_user_id=None):
    conn = get_conn()
    try:
        cur = conn.cursor()
        if exclude_user_id is None:
            cur.execute("SELECT id FROM users WHERE phone=%s", (phone,))
        else:
            cur.execute("SELECT id FROM users WHERE phone=%s AND id<>%s", (phone, exclude_user_id))
        row = cur.fetchone()
        return row is not None
    finally:
        put_conn(conn)

def update_user(user_id, nickname=None, phone=None, default_city_id=None):
    fields = []
    values = []
    if nickname is not None:
        fields.append("nickname=%s")
        values.append(nickname)
    if phone is not None:
        if phone_exists(phone, exclude_user_id=user_id):
            return None, "conflict"
        fields.append("phone=%s")
        values.append(phone)
    if default_city_id is not None:
        fields.append("default_city_id=%s")
        values.append(default_city_id)
    if not fields:
        return None, "bad_request"
    conn = get_conn()
    try:
        cur = conn.cursor()
        values.append(user_id)
        sql = "UPDATE users SET " + ", ".join(fields) + " WHERE id=%s"
        cur.execute(sql, tuple(values))
        conn.commit()
        return get_by_id(user_id), None
    finally:
        put_conn(conn)

def update_tag(user_id, tag):
    allowed = {"normal", "elderly", "children", "asthma", "pregnant"}
    if tag not in allowed:
        return None, "bad_request"
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE users SET tag=%s WHERE id=%s", (tag, user_id))
        conn.commit()
        return get_by_id(user_id), None
    finally:
        put_conn(conn)
