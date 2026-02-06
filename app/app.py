from flask import Flask, request, jsonify, render_template
from config.db_config import get_db_connection
import logging

print("✅ Flask file loaded")

app = Flask(__name__)

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def get_cursor():
    db = get_db_connection()
    return db, db.cursor(dictionary=True)

# -------------------------
# Routes
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/employees", methods=["GET"])
def get_employees():
    db, cursor = get_cursor()
    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.json
    name = data.get("name")
    role = data.get("role")

    db, cursor = get_cursor()
    cursor.execute(
        "INSERT INTO employees (name, role) VALUES (%s, %s)",
        (name, role)
    )
    db.commit()
    db.close()

    return jsonify({"message": "Employee added"})

@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    db, cursor = get_cursor()
    cursor.execute(
        "DELETE FROM employees WHERE id = %s",
        (emp_id,)
    )
    db.commit()
    db.close()
    return jsonify({"message": f"Employee {emp_id} deleted sucxcessfully"})

# -------------------------
# PRINT ROUTES & START SERVER
# -------------------------
print("🔥 REGISTERED ROUTES:")
print(app.url_map)

if __name__ == "__main__":
    print("🚀 Starting Flask server on http://127.0.0.1:5000")
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
