from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="ERP",
    user="postgres",
    password="thani123",
    host="localhost",
    port="5432"
)

@app.route('/api')
def hello_world():
    return jsonify(message="Hello from Flask!")

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    cur = conn.cursor()
    cur.execute("SELECT user_id, name, email, password_hash FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 401

    # Here password_hash column is being used to store role/password
    if password == user[3]:
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "role": user[3]
            }
        })
    else:
        return jsonify({"success": False, "message": "Invalid password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
