from backend.app.extensions.db import get_conn, put_conn
from datetime import datetime

def save_air_quality_data(city_id, recorded_time, aqi=None, aqi_level=None, dominant_pol=None,
                         pm25=None, pm10=None, o3=None, no2=None, so2=None, co=None,
                         source=None, attribution=None):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO air_quality_data
            (city_id, recorded_time, aqi, aqi_level, dominant_pol, pm25, pm10, o3, no2, so2, co, source, attribution)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (city_id, recorded_time) DO UPDATE SET
            aqi=EXCLUDED.aqi, aqi_level=EXCLUDED.aqi_level, dominant_pol=EXCLUDED.dominant_pol,
            pm25=EXCLUDED.pm25, pm10=EXCLUDED.pm10, o3=EXCLUDED.o3, no2=EXCLUDED.no2,
            so2=EXCLUDED.so2, co=EXCLUDED.co, source=EXCLUDED.source, attribution=EXCLUDED.attribution
            RETURNING id
        """, (city_id, recorded_time, aqi, aqi_level, dominant_pol, pm25, pm10, o3, no2, so2, co, source, attribution))
        
        data_id = cur.fetchone()[0]
        conn.commit()
        return data_id, None
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        put_conn(conn)

def query_air_quality_data(city_id, start_time=None, end_time=None, pollutant=None, page=1, page_size=20):
    conn = get_conn()
    try:
        cur = conn.cursor()
        
        where_clauses = ["city_id=%s"]
        params = [city_id]
        
        if start_time:
            where_clauses.append("recorded_time >= %s")
            params.append(start_time)
        
        if end_time:
            where_clauses.append("recorded_time <= %s")
            params.append(end_time)
        
        where_sql = " AND ".join(where_clauses)
        
        count_sql = f"SELECT COUNT(*) FROM air_quality_data WHERE {where_sql}"
        cur.execute(count_sql, params)
        total = cur.fetchone()[0]
        
        offset = (page - 1) * page_size
        query_sql = f"""
            SELECT id, city_id, recorded_time, aqi, aqi_level, dominant_pol, 
                   pm25, pm10, o3, no2, so2, co, source, attribution
            FROM air_quality_data
            WHERE {where_sql}
            ORDER BY recorded_time DESC
            LIMIT %s OFFSET %s
        """
        params.extend([page_size, offset])
        cur.execute(query_sql, params)
        
        items = []
        for row in cur.fetchall():
            items.append({
                "id": row[0],
                "city_id": row[1],
                "recorded_time": row[2].isoformat() if row[2] else None,
                "aqi": row[3],
                "aqi_level": row[4],
                "dominant_pol": row[5],
                "pm25": float(row[6]) if row[6] else None,
                "pm10": float(row[7]) if row[7] else None,
                "o3": float(row[8]) if row[8] else None,
                "no2": float(row[9]) if row[9] else None,
                "so2": float(row[10]) if row[10] else None,
                "co": float(row[11]) if row[11] else None,
                "source": row[12],
                "attribution": row[13],
            })
        
        return items, total, None
    except Exception as e:
        return [], 0, str(e)
    finally:
        put_conn(conn)

def get_latest_air_quality(city_id):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, city_id, recorded_time, aqi, aqi_level, dominant_pol, 
                   pm25, pm10, o3, no2, so2, co, source, attribution
            FROM air_quality_data
            WHERE city_id=%s
            ORDER BY recorded_time DESC
            LIMIT 1
        """, (city_id,))
        
        row = cur.fetchone()
        if not row:
            return None
        
        return {
            "id": row[0],
            "city_id": row[1],
            "recorded_time": row[2].isoformat() if row[2] else None,
            "aqi": row[3],
            "aqi_level": row[4],
            "dominant_pol": row[5],
            "pm25": float(row[6]) if row[6] else None,
            "pm10": float(row[7]) if row[7] else None,
            "o3": float(row[8]) if row[8] else None,
            "no2": float(row[9]) if row[9] else None,
            "so2": float(row[10]) if row[10] else None,
            "co": float(row[11]) if row[11] else None,
            "source": row[12],
            "attribution": row[13],
        }
    finally:
        put_conn(conn)

def get_monthly_stats(city_id, months=12):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                DATE_TRUNC('month', recorded_time) as month,
                COUNT(CASE WHEN aqi_level IN ('Excellent', 'Good') THEN 1 END)::float / 
                NULLIF(COUNT(*), 0) as good_ratio,
                AVG(pm25) as pm25_avg
            FROM air_quality_data
            WHERE city_id=%s
            GROUP BY DATE_TRUNC('month', recorded_time)
            ORDER BY month DESC
            LIMIT %s
        """, (city_id, months))
        
        items = []
        for row in cur.fetchall():
            items.append({
                "month": row[0].strftime("%Y-%m") if row[0] else None,
                "good_ratio": float(row[1]) if row[1] else 0.0,
                "pm25_avg": float(row[2]) if row[2] else None,
            })
        
        return items, None
    except Exception as e:
        return [], str(e)
    finally:
        put_conn(conn)
