from flask_mysqldb import MySQL
import re
import os
from validation.user_data_format import *
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    jsonify,
    url_for,
    request,
    session,
)
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

        # Format RUT to delete spaces and hyphens
        rut = format_rut(request.form.get("rut"))

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
            flash(
                "La contraseña y la contraseña de confirmación no coinciden", "warning"
            )
            return render_template("register.html")

        # Ensure password has at least two digits and three letters
        password = request.form.get("password")
        digits = re.findall(r"\d", password)
        letters = re.findall(r"[A-Za-z]", password)

        if not (len(digits) >= 2 and len(letters) >= 3):
            flash(
                "La contraseña debe contener al menos 3 letras y 2 dígitos", "warning"
            )
            return render_template("register.html")

        # Format RUT, mail, and name
        rut, mail, name = format_data(
            request.form.get("rut"), request.form.get("mail"), request.form.get("name")
        )

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
                (
                    rut,
                    name,
                    mail,
                    "normal",
                    generate_password_hash(request.form.get("password")),
                ),
            )
            mysql.connection.commit()
        except Exception as e:
            # Handle the exception
            print("Error al intentar registrar el usuario:", e)
            flash("Error al registrar el usuario", "warning")
            return render_template("register.html")
        finally:
            cursor.close()

        flash("Usuario creado correctamente", "success")
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/biblioteca", methods=["GET"])
def biblioteca():
    order = request.args.get("o", default="titulo")
    direction = request.args.get("d", default="ASC").upper()

    cursor = mysql.connection.cursor()
    valid_columns = ["titulo", "autor", "anio", "genero", "stock"]
    if order in valid_columns and direction in ["ASC", "DESC"]:
        # Construir la consulta SQL asegurando que el valor de 'order' sea seguro
        query = f"SELECT * FROM Book ORDER BY {order} {direction}"
    else:
        # Ordenamiento predeterminado si los parámetros no son válidos
        query = "SELECT * FROM Book ORDER BY titulo ASC"

    cursor.execute(query)
    books = cursor.fetchall()
    cursor.close()

    # Si la solicitud es AJAX, entonces devolvemos JSON
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"books": books})

    # Si no, renderizamos la página con los libros
    return render_template("biblioteca.html", books=books)


if __name__ == "__main__":
    app.run(debug=True)
