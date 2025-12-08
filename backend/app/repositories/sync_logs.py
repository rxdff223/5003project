from backend.app.extensions.db import get_conn, put_conn
from datetime import datetime
import json

def log_sync(sync_type, data_source, start_time=None, status="in_progress", error_message=None, details=None):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO sync_logs
            (sync_type, data_source, start_time, status, error_message, details)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (sync_type, data_source, start_time or datetime.utcnow(), status, error_message, 
              json.dumps(details) if details else None))
        
        log_id = cur.fetchone()[0]
        conn.commit()
        return log_id, None
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        put_conn(conn)

def update_sync_log(log_id, end_time=None, success_count=None, fail_count=None, total_count=None,
                   status=None, error_message=None, details=None):
    fields = []
    values = []
    
    if end_time is not None:
        fields.append("end_time=%s")
        values.append(end_time)
    if success_count is not None:
        fields.append("success_count=%s")
        values.append(success_count)
    if fail_count is not None:
        fields.append("fail_count=%s")
        values.append(fail_count)
    if total_count is not None:
        fields.append("total_count=%s")
        values.append(total_count)
    if status is not None:
        fields.append("status=%s")
        values.append(status)
    if error_message is not None:
        fields.append("error_message=%s")
        values.append(error_message)
    if details is not None:
        fields.append("details=%s")
        values.append(json.dumps(details))
    
    if not fields:
        return None, "no_fields"
    
    conn = get_conn()
    try:
        cur = conn.cursor()
        values.append(log_id)
        sql = "UPDATE sync_logs SET " + ", ".join(fields) + " WHERE id=%s"
        cur.execute(sql, tuple(values))
        conn.commit()
        return log_id, None
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        put_conn(conn)

def get_sync_logs(start_date=None, end_date=None, page=1, page_size=20):
    conn = get_conn()
    try:
        cur = conn.cursor()
        
        where_clauses = []
        params = []
        
        if start_date:
            where_clauses.append("DATE(created_at) >= %s")
            params.append(start_date)
        
        if end_date:
            where_clauses.append("DATE(created_at) <= %s")
            params.append(end_date)
        
        where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        count_sql = f"SELECT COUNT(*) FROM sync_logs{where_sql}"
        cur.execute(count_sql, params)
        total = cur.fetchone()[0]
        
        offset = (page - 1) * page_size
        query_sql = f"""
            SELECT id, sync_type, data_source, start_time, end_time, success_count, fail_count,
                   total_count, status, error_message, created_at
            FROM sync_logs{where_sql}
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        params.extend([page_size, offset])
        cur.execute(query_sql, params)
        
        items = []
        for row in cur.fetchall():
            duration = None
            if row[3] and row[4]:
                duration = (row[4] - row[3]).total_seconds()
            
            items.append({
                "id": row[0],
                "sync_type": row[1],
                "data_source": row[2],
                "start_time": row[3].isoformat() if row[3] else None,
                "end_time": row[4].isoformat() if row[4] else None,
                "success_count": row[5],
                "fail_count": row[6],
                "total_count": row[7],
                "status": row[8],
                "error_message": row[9],
                "duration_seconds": duration,
                "created_at": row[10].isoformat() if row[10] else None,
            })
        
        return items, total, None
    except Exception as e:
        return [], 0, str(e)
    finally:
        put_conn(conn)

def get_sync_stats(days=7):
    conn = get_conn()
    try:
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                COUNT(*) as total_count,
                SUM(CASE WHEN status='success' THEN 1 ELSE 0 END) as success_count,
                SUM(success_count) as total_success_data,
                SUM(fail_count) as total_fail_data,
                AVG(EXTRACT(EPOCH FROM (end_time - start_time))) as avg_duration
            FROM sync_logs
            WHERE created_at >= NOW() - INTERVAL '%s days'
        """, (days,))
        
        row = cur.fetchone()
        if row:
            success_rate = (row[1] / row[0] * 100) if row[0] > 0 else 0
            return {
                "total_syncs": row[0] or 0,
                "success_syncs": row[1] or 0,
                "success_rate": success_rate,
                "total_success_data": row[2] or 0,
                "total_fail_data": row[3] or 0,
                "average_duration_seconds": float(row[4]) if row[4] else None,
            }, None
        
        return {
            "total_syncs": 0,
            "success_syncs": 0,
            "success_rate": 0,
            "total_success_data": 0,
            "total_fail_data": 0,
            "average_duration_seconds": None,
        }, None
    except Exception as e:
        return {}, str(e)
    finally:
        put_conn(conn)
