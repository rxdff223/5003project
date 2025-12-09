from backend.app.extensions.db import get_conn, put_conn

def get_all_cities(q=None, province=None, page=1, page_size=20):
    conn = get_conn()
    try:
        cur = conn.cursor()
        
        where_clauses = []
        params = []
        
        if q:
            where_clauses.append("LOWER(name) LIKE LOWER(%s)")
            params.append(f"%{q}%")
        
        if province:
            where_clauses.append("province = %s")
            params.append(province)
        
        where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        count_sql = f"SELECT COUNT(*) FROM cities{where_sql}"
        cur.execute(count_sql, params)
        total = cur.fetchone()[0]
        
        offset = (page - 1) * page_size
        query_sql = f"SELECT id, name, province, lat, lon FROM cities{where_sql} ORDER BY name LIMIT %s OFFSET %s"
        params.extend([page_size, offset])
        cur.execute(query_sql, params)
        
        items = []
        for row in cur.fetchall():
            items.append({
                "id": row[0],
                "name": row[1],
                "province": row[2],
                "lat": float(row[3]) if row[3] else None,
                "lon": float(row[4]) if row[4] else None,
            })
        
        return items, total, None
    except Exception as e:
        return [], 0, str(e)
    finally:
        put_conn(conn)

def get_city_by_id(city_id):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, province, lat, lon FROM cities WHERE id=%s", (city_id,))
        row = cur.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "name": row[1],
            "province": row[2],
            "lat": float(row[3]) if row[3] else None,
            "lon": float(row[4]) if row[4] else None,
        }
    finally:
        put_conn(conn)

def create_city(name, province=None, lat=None, lon=None):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO cities(name, province, lat, lon) VALUES (%s, %s, %s, %s) RETURNING id",
            (name, province, lat, lon)
        )
        city_id = cur.fetchone()[0]
        conn.commit()
        return get_city_by_id(city_id), None
    except Exception as e:
        return None, str(e)
    finally:
        put_conn(conn)

def update_city(city_id, name=None, province=None, lat=None, lon=None):
    fields = []
    values = []
    
    if name is not None:
        fields.append("name=%s")
        values.append(name)
    if province is not None:
        fields.append("province=%s")
        values.append(province)
    if lat is not None:
        fields.append("lat=%s")
        values.append(lat)
    if lon is not None:
        fields.append("lon=%s")
        values.append(lon)
    
    if not fields:
        return None, "no_fields"
    
    conn = get_conn()
    try:
        cur = conn.cursor()
        values.append(city_id)
        sql = "UPDATE cities SET " + ", ".join(fields) + " WHERE id=%s"
        cur.execute(sql, tuple(values))
        conn.commit()
        return get_city_by_id(city_id), None
    except Exception as e:
        return None, str(e)
    finally:
        put_conn(conn)

def delete_city(city_id):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM cities WHERE id=%s", (city_id,))
        conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        put_conn(conn)
