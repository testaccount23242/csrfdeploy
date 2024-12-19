# app.py
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, session, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = "super_secret_key"

DB_URL = "postgresql://csrf_db_user:DusFfExrvmbRfQxWBG7qUtwo30TczsSU@dpg-ctem62pu0jms739dbqi0-a.oregon-postgres.render.com/csrf_db"

def get_db_connection():
    conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
    return conn

def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            with open('schema.sql') as f:
                cursor.execute(f.read())
            print("Database initialized.")

# @app.before_request
# def setup_database():
#     pass
# Routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
                user = cursor.fetchone()
        if user:
            session["username"] = username
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))
        return "Invalid credentials!", 401
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"], role=session["role"])

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "username" not in session or session["role"] != "admin":
        return redirect(url_for("login"))
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
    if request.method == "POST":
        user_id = request.form["user_id"]
        role = request.form["role"]
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('UPDATE users SET role = %s WHERE username = %s', (role, user_id))
                conn.commit()
        return "Role updated successfully!"
    return render_template("admin.html", users=users)

@app.route("/flag")
def flag():
    if "username" in session and session["role"] == "admin":
        return render_template("flag.html")
    return "Access Denied", 403

if __name__ == "__main__":
    init_db()  
    app.run(debug=True)
