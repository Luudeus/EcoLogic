from flask_mysqldb import MySQL
import re
import os
from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, jsonify, url_for, request, session
from flask_session import Session
from functions import login_required
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Load environment variables from .env
load_dotenv()

# Configure Flask-MySQLdb
app.config["MYSQL_HOST"] = os.getenv("DB_HOST")
app.config["MYSQL_USER"] = os.getenv("DB_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("DB_PASS")
app.config["MYSQL_DB"] = os.getenv("DB_NAME")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Initialize MySQL
mysql = MySQL(app)


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
    """Show FuturaLib's homepage"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    # Forget any user_id
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure rut was submitted
        if not request.form.get("rut"):
            flash("Se debe ingresar el RUT", "warning")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Se debe ingresar la contraseña", "warning")
            return render_template("login.html")

        # Procesa el RUT para eliminar puntos y guión
        rut = request.form.get("rut").replace(".", "").replace("-", "")

         # Create a new database cursor
        cursor = mysql.connection.cursor()

        # Query database for rut
        cursor.execute("SELECT * FROM User WHERE RUT = %s", (rut,))
        rows = cursor.fetchall()

        # Ensure rut exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["contrasenia"], request.form.get("password")
        ):
            flash("RUT y/o contraseña inválidos", "warning")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["RUT"]

        # Close the db cursor
        cursor.close()
        
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
        # Ensure rut was submitted
        if not request.form.get("rut"):
            flash("Se debe ingresar el RUT", "warning")
            return render_template("register.html")
        
        # Ensure name was submitted
        elif not request.form.get("name"):
            flash("Se debe ingresar el nombre", "warning")
            return render_template("register.html")
        
        # Ensure mail was submitted
        elif not request.form.get("mail"):
            flash("Se debe ingresar el correo", "warning")
            return render_template("register.html")
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Se debe ingresar la contraseña", "warning")
            return render_template("register.html")

        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation"):
            flash("Se debe re-ingresar la contraseña", "warning")
            return render_template("register.html")

        # Check if passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            flash("La contraseña y la contraseña de confirmación no coinciden", "warning")
            return render_template("register.html")

        # Ensure password has at least two digits and three letters
        password = request.form.get("password")
        digits = re.findall(r"\d", password)
        letters = re.findall(r"[A-Za-z]", password)

        if not (len(digits) >= 2 and len(letters) >= 3):
            flash("La contraseña debe contener al menos 3 letras y 2 dígitos", "warning")
            return render_template("register.html")
        
        # Format RUT to delete dots and hyphens
        rut = request.form.get("rut").replace(".", "").replace("-", "")

        # Check if rut is available
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("SELECT * FROM User WHERE RUT = %s", (rut,))
            rows = cursor.fetchall()
            if len(rows) > 0:
                flash("El usuario ya existe", "warning")
                return render_template("register.html")
        finally:
            cursor.close()

        # Insert the user into the users table
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO User (RUT, nombre, correo, permisos, contrasenia) VALUES (%s, %s, %s, %s, %s)",
                (rut, request.form.get("name"), request.form.get("mail"), "normal", generate_password_hash(request.form.get("password"))),
            )
            mysql.connection.commit()
        except Exception as e:
            # Handle the exception
            flash("Error al registrar el usuario", "warning")
            return render_template("register.html")
        finally:
            cursor.close()

        return redirect("/")
    
    
@app.route("/biblioteca", methods=['GET', 'POST'])
def biblioteca():
    """
    Handle requests to the library page. 
    On GET request, render the library page.
    On POST request, perform book search and filtering.
    """
    if request.method == 'GET':
        # Connect to the database and fetch initial set of books
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Book")
            initial_books = cursor.fetchall()
        finally:
            cursor.close()

        # Render the library page template with initial books
        return render_template('biblioteca.html', books=initial_books)

    # Retrieve query parameters for search and filtering
    query = request.args.get('query', '')
    filter_type = request.args.get('filter', 'all')

    # Connect to the database and execute the query based on the filter type
    cursor = mysql.connection.cursor()
    try:
        if filter_type == 'titulo':
            cursor.execute("SELECT * FROM Book WHERE titulo LIKE %s", ('%' + query + '%',))
        elif filter_type == 'autor':
            cursor.execute("SELECT * FROM Book WHERE autor LIKE %s", ('%' + query + '%',))
        elif filter_type == 'anio':
            cursor.execute("SELECT * FROM Book WHERE anio = %s", (query,))
        elif filter_type == 'genero':
            cursor.execute("SELECT * FROM Book WHERE genero LIKE %s", ('%' + query + '%',))
        else:
            cursor.execute("SELECT * FROM Book WHERE title LIKE %s OR author LIKE %s", ('%' + query + '%', '%' + query + '%'))

        books = cursor.fetchall()
    finally:
        cursor.close()

    # Send the results back in JSON format
    return jsonify({"books": books})

if __name__ == "__main__":
    app.run(debug=True)