import os
import mysql.connector
from urllib.parse import urlparse

url = urlparse(os.environ.get("MYSQL_URL"))

db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path.lstrip('/'),
    port=url.port
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