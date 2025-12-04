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
