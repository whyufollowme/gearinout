from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import os  # added for path handling

app = Flask(__name__)
app.secret_key = "supersecretpassword"  # Needed for sessions

# --- Set absolute path for DB ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where app.py lives
DB = os.path.join(BASE_DIR, 'database', 'gear.db')     # points to database/gear.db inside app folder

ADMIN_PASSWORD = "1234"  # Simple admin password

# --- Database connection ---
def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# --- Student login ---
@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    if request.method == "POST":
        student_id = request.form["student"]
        return redirect(url_for("scan_gear", student_id=student_id))
    return render_template("index.html", students=students)

# --- Gear scan / checkout ---
@app.route("/scan-gear/<student_id>", methods=["GET", "POST"])
def scan_gear(student_id):
    conn = get_db_connection()
    student = conn.execute("SELECT name FROM students WHERE id=?", (student_id,)).fetchone()
    if not student:
        conn.close()
        return "Student not found", 404
    student_name = student["name"]

    # Gear currently checked out by this student
    checked_out_gear = conn.execute(
        "SELECT * FROM gear WHERE status LIKE ?",
        (f"out ({student_name})%",)
    ).fetchall()

    # Gear available for checkout
    available_gear = conn.execute(
        "SELECT * FROM gear WHERE status='available'"
    ).fetchall()

    if request.method == "POST":
        gear_id = request.form["gear"]
        gear = conn.execute("SELECT status FROM gear WHERE id=?", (gear_id,)).fetchone()

        if gear["status"] == "available":
            # Check out
            conn.execute(
                "INSERT INTO transactions (student_id, gear_id, timestamp_out, status) VALUES (?, ?, ?, ?)",
                (student_id, gear_id, datetime.now(), "out")
            )
            conn.execute(
                "UPDATE gear SET status=? WHERE id=?",
                (f"out ({student_name})", gear_id)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
        else:
            # Check in
            conn.execute(
                "UPDATE gear SET status='available' WHERE id=?",
                (gear_id,)
            )
            conn.execute(
                "UPDATE transactions SET timestamp_in=?, status='in' WHERE gear_id=? AND student_id=? AND status='out'",
                (datetime.now(), gear_id, student_id)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    conn.close()
    return render_template("scan_gear.html", student_name=student_name,
                           checked_out_gear=checked_out_gear, available_gear=available_gear)

# --- Admin login ---
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"]
        if password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Incorrect password!")
    return render_template("admin_login.html")

# --- Admin dashboard ---
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    gear = conn.execute("SELECT * FROM gear").fetchall()
    transactions = conn.execute("SELECT * FROM transactions").fetchall()
    conn.close()

    return render_template("dashboard.html", students=students, gear=gear, transactions=transactions)

# --- Add student ---
@app.route("/admin/add-student", methods=["GET", "POST"])
def add_student():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        name = request.form["name"]
        barcode = request.form["barcode"]
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO students (name, barcode) VALUES (?, ?)",
            (name, barcode)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("admin_dashboard"))

    return render_template("add_student.html")

# --- Remove student ---
@app.route("/admin/remove-student", methods=["GET", "POST"])
def remove_student():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    if request.method == "POST":
        student_id = request.form["student"]
        conn = get_db_connection()
        conn.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("admin_dashboard"))

    return render_template("remove_student.html", students=students)

# --- Add gear ---
@app.route("/admin/add-gear", methods=["GET", "POST"])
def add_gear():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        name = request.form["name"]
        barcode = request.form["barcode"]
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO gear (name, barcode) VALUES (?, ?)",
            (name, barcode)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("admin_dashboard"))

    return render_template("add_gear.html")

# --- Remove gear ---
@app.route("/admin/remove-gear", methods=["GET", "POST"])
def remove_gear():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    gear_list = conn.execute("SELECT * FROM gear").fetchall()
    conn.close()

    if request.method == "POST":
        gear_id = request.form["gear"]
        conn = get_db_connection()
        conn.execute("DELETE FROM gear WHERE id=?", (gear_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("admin_dashboard"))

    return render_template("remove_gear.html", gear_list=gear_list)
#admin set gear
@app.route("/admin/set-gear-status", methods=["GET", "POST"])
def set_gear_status():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    gear_list = conn.execute("SELECT * FROM gear").fetchall()
    conn.close()

    if request.method == "POST":
        gear_id = request.form["gear"]
        new_status = request.form["status"]
        conn = get_db_connection()
        conn.execute("UPDATE gear SET status=? WHERE id=?", (new_status, gear_id))
        conn.commit()
        conn.close()
        return redirect(url_for("admin_dashboard"))

    return render_template("set_gear_status.html", gear_list=gear_list)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

