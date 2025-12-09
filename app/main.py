from fastapi import FastAPI
import os
import psycopg2
import time

app = FastAPI()

# Database configuration
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "demo")
DB_USER = os.getenv("POSTGRES_USER", "demo")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "demopw")

_port = os.getenv("POSTGRES_PORT", "5432")
DB_PORT = int(_port.split(":")[-1]) if "://" in _port else int(_port)

def get_db():
    """Get database connection with retries"""
    for attempt in range(5):
        try:
            return psycopg2.connect(
                host=DB_HOST, dbname=DB_NAME, user=DB_USER, 
                password=DB_PASS, port=DB_PORT
            )
        except Exception as e:
            if attempt < 4:
                print(f"DB connection failed (attempt {attempt+1}/5): {e}")
                time.sleep(1)
            else:
                return None

@app.get("/hello")
def hello():
    return {"message": "Hello from FastAPI"}

@app.get("/db-count")
def db_count():
    """Get and increment hit count from database"""
    conn = get_db()
    if not conn:
        return {"error": "cannot connect to db"}
    
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS hits (id serial PRIMARY KEY, ts timestamptz DEFAULT now())")
                cur.execute("INSERT INTO hits DEFAULT VALUES")
                cur.execute("SELECT count(*) FROM hits")
                count = cur.fetchone()[0]
        return {"hits": count}
    except Exception as e:
        return {"error": str(e)}
