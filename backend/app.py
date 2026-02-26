from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# Database connection
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",  # Put your MySQL password if you have one
    database="portfolio"
)

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json
    
    cursor = connection.cursor()
    sql = "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (data["name"], data["email"], data["message"]))
    connection.commit()

    return jsonify({"message": "Saved successfully"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)