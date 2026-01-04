from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask import session
from db import get_db_connection, init_db
from classifier import classify_complaint
import sqlite3

app = Flask(__name__)

app.secret_key = "community-pulse-secret"

ADMIN_PASSWORD = "admin123"

# Initialize DB
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    role = request.form.get("role")
    visibility = request.form.get("visibility") or "Private"
    complaint_text = request.form.get("complaint")

    category, urgency = classify_complaint(complaint_text)
    status = "New"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db_connection()
    conn.execute(
        """INSERT INTO complaints
           (name, role, text, category, urgency, status, visibility, upvotes, timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (name, role, complaint_text, category, urgency, status, visibility, 0, timestamp)
    )
    conn.commit()
    conn.close()

    return redirect("/?success=1")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            return redirect("/admin")
        error = "Incorrect password"
    return render_template("login.html", error=error)

@app.route("/admin")
def admin():
    conn = sqlite3.connect("complaints.db")
    conn.row_factory = sqlite3.Row

    urgency = request.args.get("urgency")

    if urgency:
        complaints = conn.execute(
            "SELECT * FROM complaints WHERE urgency = ? ORDER BY id DESC",
            (urgency,)
        ).fetchall()
    else:
        complaints = conn.execute(
            "SELECT * FROM complaints ORDER BY id DESC"
        ).fetchall()

    conn.close()
    return render_template("admin.html", complaints=complaints)

@app.route("/update_status/<int:cid>", methods=["POST"])
def update_status(cid):
    new_status = request.form.get("status")
    conn = get_db_connection()
    conn.execute(
        "UPDATE complaints SET status = ? WHERE id = ?",
        (new_status, cid)
    )
    conn.commit()
    conn.close()
    return redirect("/admin")

@app.route("/community")
def community():
    conn = get_db_connection()
    complaints = conn.execute(
        "SELECT * FROM complaints WHERE visibility='Public' ORDER BY upvotes DESC"
    ).fetchall()
    conn.close()
    return render_template("community.html", complaints=complaints)


@app.route("/upvote/<int:complaint_id>", methods=["POST"])
def upvote(complaint_id):
    # Initialize upvote tracker in session
    if "upvoted" not in session:
        session["upvoted"] = []

    # Prevent multiple upvotes for same complaint
    if complaint_id in session["upvoted"]:
        return redirect("/community")

    # Register upvote
    conn = get_db_connection()
    conn.execute(
        "UPDATE complaints SET upvotes = upvotes + 1 WHERE id = ?",
        (complaint_id,)
    )
    conn.commit()
    conn.close()

    # Store that this complaint was upvoted
    session["upvoted"].append(complaint_id)
    session.modified = True

    return redirect("/community")



import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

