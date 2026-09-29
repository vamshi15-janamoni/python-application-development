from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "database/app.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )""")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Python REST API is running"})

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(dict(user))

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "name and email are required"}), 400
    try:
        conn = get_db()
        cur = conn.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                           (data["name"], data["email"]))
        conn.commit()
        user_id = cur.lastrowid
        conn.close()
        return jsonify({"message": "User created successfully", "id": user_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "name and email are required"}), 400
    conn = get_db()
    cur = conn.execute("UPDATE users SET name = ?, email = ? WHERE id = ?",
                       (data["name"], data["email"], user_id))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User updated successfully"})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db()
    cur = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
