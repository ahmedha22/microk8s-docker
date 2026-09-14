import os

import psycopg
from flask import Flask, jsonify

app = Flask(__name__)


def database_status():
    try:
        with psycopg.connect(
            host=os.getenv("DB_HOST", "localhost"),
            dbname=os.getenv("DB_NAME", "appdb"),
            user=os.getenv("DB_USER", "appuser"),
            password=os.getenv("DB_PASSWORD", "local-dev-password"),
            connect_timeout=3,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        return "connected"
    except Exception:
        return "unavailable"


@app.get("/")
def home():
    return jsonify({
        "app": "platform-api",
        "message": "Docker and Kubernetes practice app",
        "author": "Ahmed Hassan",
        "version": "v2-change-test",
    })


@app.get("/health")
def health():
    return jsonify({"status": "ok", "database": database_status()})


@app.get("/products")
def products():
    with psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "appdb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "local-dev-password"),
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, price_cents FROM products ORDER BY id")
            rows = cursor.fetchall()

    return jsonify([
        {"id": product_id, "name": name, "price_cents": price_cents}
        for product_id, name, price_cents in rows
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
