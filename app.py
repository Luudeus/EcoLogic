import mysql.connector as SQL
import re
from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_session import Session
from functions import login_required
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure mysql.connector library to use MySQL database
db = SQL.connect(
    host="localhost",
    user="user",
    password="password",
    database="database"
)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show EcoLogic's homepage"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    # Forget any user_id
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username", "warning")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password", "warning")
            return render_template("login.html")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("Invalid username and/or password", "warning")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username", "warning")
            return render_template("register.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password", "warning")
            return render_template("register.html")

        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation"):
            flash("Must re-enter password", "warning")
            return render_template("register.html")

        # Check if passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            flash("Password and confirmation password don't match", "warning")
            return render_template("register.html")

        # Ensure password has at least two digits and three letters
        password = request.form.get("password")
        digits = re.findall(r"\d", password)
        letters = re.findall(r"[A-Za-z]", password)

        if not (len(digits) >= 2 and len(letters) >= 3):
            flash("Password must contain at least 3 letters and 2 digits", "warning")
            return render_template("register.html")

        # Check is username's is available
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 0:
            flash("Username already exists", "warning")
            return render_template("register.html")

        # Insert the user into the users table
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )

        return redirect("/")