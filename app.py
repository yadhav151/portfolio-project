import os
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host=os.getenv("mysql.railway.internal"),
    user=os.getenv("root"),
    password=os.getenv("OtmzInrhblxgtvKrmEKijUGvxPZeJqaW"),
    database=os.getenv("railway"),
    port=int(os.getenv("3306", 3306))
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