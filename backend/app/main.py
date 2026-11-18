import os
from urllib.parse import urlparse

import pg8000.native
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
app = FastAPI(title="VeriFinance AI")


def get_conn():
    u = urlparse(os.environ["DATABASE_URL"])
    return pg8000.native.Connection(
        user=u.username,
        password=u.password,
        host=u.hostname,
        port=u.port or 5432,
        database=u.path.lstrip("/"),
    )


@app.get("/health")
def health():
    conn = get_conn()
    try:
        rows = conn.run("SELECT extname FROM pg_extension WHERE extname='vector'")
    finally:
        conn.close()
    return {"status": "ok", "pgvector": bool(rows)}
