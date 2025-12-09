from backend.app.extensions.db import get_conn, put_conn
from datetime import datetime, date
import json

def log_user_action(user_id, action_type, city_id=None, details=None):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO user_analytics
            (user_id, action_date, action_type, city_id, details)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (user_id, date.today(), action_type, city_id, json.dumps(details) if details else None))
        
        analytics_id = cur.fetchone()[0]
        conn.commit()
        return analytics_id, None
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        put_conn(conn)

def get_dau_stats(start_date, end_date):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT action_date, COUNT(DISTINCT user_id) as dau
            FROM user_analytics
            WHERE action_date >= %s AND action_date <= %s AND user_id IS NOT NULL
            GROUP BY action_date
            ORDER BY action_date DESC
        """, (start_date, end_date))
        
        items = []
        for row in cur.fetchall():
            items.append({
                "date": row[0].isoformat() if row[0] else None,
                "dau": row[1],
            })
        
        return items, None
    except Exception as e:
        return [], str(e)
    finally:
        put_conn(conn)

def get_top_cities(start_date, end_date, limit=5):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.id, c.name, COUNT(*) as count
            FROM user_analytics ua
            LEFT JOIN cities c ON ua.city_id = c.id
            WHERE ua.action_date >= %s AND ua.action_date <= %s AND ua.city_id IS NOT NULL
            GROUP BY c.id, c.name
            ORDER BY count DESC
            LIMIT %s
        """, (start_date, end_date, limit))
        
        items = []
        for row in cur.fetchall():
            items.append({
                "city_id": row[0],
                "city_name": row[1],
                "count": row[2],
            })
        
        return items, None
    except Exception as e:
        return [], str(e)
    finally:
        put_conn(conn)

def get_feature_usage(start_date, end_date):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT action_type, COUNT(*) as count
            FROM user_analytics
            WHERE action_date >= %s AND action_date <= %s
            GROUP BY action_type
            ORDER BY count DESC
        """, (start_date, end_date))
        
        items = []
        for row in cur.fetchall():
            items.append({
                "feature": row[0],
                "count": row[1],
            })
        
        return items, None
    except Exception as e:
        return [], str(e)
    finally:
        put_conn(conn)

def get_health_advice(pollutant=None, aqi_level=None, target_group=None):
    conn = get_conn()
    try:
        cur = conn.cursor()
        
        where_clauses = ["is_active = TRUE"]
        params = []
        
        if pollutant:
            where_clauses.append("pollutant = %s")
            params.append(pollutant)
        
        if aqi_level:
            where_clauses.append("aqi_level = %s")
            params.append(aqi_level)
        
        if target_group:
            where_clauses.append("target_group = %s")
            params.append(target_group)
        
        where_sql = " AND ".join(where_clauses)
        
        query_sql = f"""
            SELECT id, pollutant, aqi_level, target_group, title, description, recommendations,
                   applicable_start_month, applicable_end_month
            FROM health_advice
            WHERE {where_sql}
            ORDER BY created_at DESC
        """
        
        cur.execute(query_sql, params)
        
        items = []
        for row in cur.fetchall():
            items.append({
                "id": row[0],
                "pollutant": row[1],
                "aqi_level": row[2],
                "target_group": row[3],
                "title": row[4],
                "description": row[5],
                "recommendations": row[6],
                "applicable_start_month": row[7],
                "applicable_end_month": row[8],
            })
        
        return items, None
    except Exception as e:
        return [], str(e)
    finally:
        put_conn(conn)
