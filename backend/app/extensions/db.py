import os
import psycopg2
import psycopg2.pool

pool = None

def init_db():
    global pool
    if pool is not None:
        return
    url = os.getenv("DATABASE_URL")
    if not url:
        url = "postgresql://postgres:postgres@localhost:5432/postgres"
    try:
        pool = psycopg2.pool.ThreadedConnectionPool(1, 10, dsn=url)
    except Exception as e:
        print(f"Warning: Database connection failed: {e}")
        print("Application will run without database. Some features may not work.")

def get_conn():
    if pool is None:
        init_db()
    if pool is None:
        raise Exception("Database pool not initialized. Database connection is not available.")
    return pool.getconn()

def put_conn(conn):
    if pool is None:
        return
    pool.putconn(conn)
