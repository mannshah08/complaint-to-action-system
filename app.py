from flask import Flask, render_template, request, redirect,session,url_for
from datetime import datetime
from db import get_db_connection, init_db
from classifier import classify_complaint
import sqlite3
from flask_dance.contrib.google import make_google_blueprint, google
import os


app = Flask(__name__)

app.secret_key = "supersecretkey"  # simple for MVP

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # allow http for local dev

google_bp = make_google_blueprint(
    client_id="1083899840316-rlfd6frjaurr1tavp9ft3h548go9i3v1.apps.googleusercontent.com",
    client_secret="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",
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email"
    ],
    redirect_to="login_success"
)

app.register_blueprint(google_bp, url_prefix="/login")

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

@app.route("/admin-auth", methods=["GET", "POST"])
def admin_auth():
    if not session.get("google_logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin"))
        else:
            return render_template("admin_login.html", error="Wrong password")

    return render_template("admin_login.html")

@app.context_processor
def inject_auth_status():
    return dict(is_logged_in=google.authorized)

# @app.route("/admin")
# def admin():
#     if not session.get("google_logged_in"):
#         return redirect(url_for("login"))

#     if not session.get("is_admin"):
#         return redirect(url_for("admin_auth"))

#     conn = sqlite3.connect("complaints.db")
#     conn.row_factory = sqlite3.Row

#     complaints = conn.execute(
#         "SELECT * FROM complaints ORDER BY id DESC"
#     ).fetchall()

#     conn.close()
#     return render_template("admin.html", complaints=complaints)

@app.route("/admin")
def admin():
    if not session.get("google_logged_in"):
        return redirect(url_for("login"))

    if not session.get("is_admin"):
        return redirect(url_for("admin_auth"))

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

@app.route("/login")
def login():
    return redirect(url_for("google.login"))

@app.route("/login/success")
def login_success():
    session["google_logged_in"] = True
    session["is_admin"] = False
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=8080, debug=True)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080, debug=True)


