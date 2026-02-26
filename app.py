import os
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT", 3306))
)
@app.route("/")
def home():
    return "Backend is running!"

@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    cursor = db.cursor()

    # MySQL table creation (correct syntax)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            message TEXT
        )
    """)

    sql = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    values = (name, email, message)

    cursor.execute(sql, values)
    db.commit()

    cursor.close()

    return jsonify({"message": "Contact saved successfully!"})