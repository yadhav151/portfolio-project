import os
from flask import Flask, request, send_from_directory, jsonify
import mysql.connector
from urllib.parse import urlparse

app = Flask(__name__, static_folder=".")

db = None

url_string = os.environ.get("MYSQL_URL")

if url_string:
    url = urlparse(url_string)

    db = mysql.connector.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path.lstrip('/'),
        port=url.port
    )
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/contact", methods=["POST"])
def contact():

    if request.is_json:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

    if not db:
        return jsonify({"error": "Database not connected"}), 500

    cursor = db.cursor()   # ← THIS WAS MISSING

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            message TEXT
        )
    """)

    sql = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, message))
    db.commit()
    cursor.close()

    return jsonify({"message": "Contact saved successfully!"})