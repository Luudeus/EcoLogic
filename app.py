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
from functions import login_required, logged_in_redirect
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
@logged_in_redirect
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
        
        # Remember permission type of the user
        session["permission_type"] = rows[0]["permisos"]

        # Close the db cursor
        cursor.close()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
@logged_in_redirect
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

    # Forget any user_id and permissions
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quienes-somos", methods=["GET"])
def quienes_somos():
    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("quienes-somos.html")
    

@app.route("/biblioteca", methods=["GET", "POST"])
def biblioteca():
    if request.method == "GET":
        order = request.args.get("o", default="titulo")
        direction = request.args.get("d", default="ASC").upper()

        cursor = mysql.connection.cursor()
        valid_columns = ["titulo", "autor", "anio", "genero", "stock"]
        if order in valid_columns and direction in ["ASC", "DESC"]:
            # Construct the SQL query ensuring the 'order' value is safe
            query = f"SELECT * FROM Book ORDER BY {order} {direction}"
        else:
            # Default ordering if the parameters are not valid
            query = "SELECT * FROM Book ORDER BY titulo ASC"

        cursor.execute(query)
        books = cursor.fetchall()
        cursor.close()

        # If the request is AJAX, then return JSON
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"books": books})

        # Otherwise, render the page with the books
        return render_template("biblioteca.html", books=books)
    else:
        # SELECT * FROM Book WHERE titulo LIKE %s
        busqueda = request.form.get("busqueda")
        
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Book WHERE titulo LIKE %s", (f"%{busqueda}%",))

        except Exception as e:
            print("No se pudo hacer la búsqueda:", e)
        books = cursor.fetchall()
        books = list(books)
        
        cursor.close()
        # Render the page with the books
        return render_template("biblioteca.html", books=books)


@app.route("/agregar-libros", methods=["GET", "POST"])
def agregar_libro():
    if request.method == "GET":
        # User reached route via GET (as by clicking a link or via redirect)
        return render_template("agregar-libros.html")
    else:
        if not request.form.get('titulo'):
            flash("Se debe introducir título.\nTodos los campos son obligarios", "warning")
            render_template("agregar-libros.html")
        elif not request.form.get('autor'):
            flash("Se debe introducir autor.\nTodos los campos son obligarios", "warning")
            render_template("agregar-libros.html")
        elif not request.form.get('anio'):
            flash("Se debe introducir año.\nTodos los campos son obligarios", "warning")
            render_template("agregar-libros.html")
        elif not request.form.get('genero'):
            flash("Se debe introducir género.\nTodos los campos son obligarios", "warning")
            render_template("agregar-libros.html")
        elif not request.form.get('stock'):
            flash("Se debe introducir stock.\nTodos los campos son obligarios", "warning")
            render_template("agregar-libros.html")
        # User reached route via POST (as by submitting a form)
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        anio = request.form.get('anio')
        genero = request.form.get('genero')
        stock = request.form.get('stock')
        print(titulo, autor, anio, genero, stock)
        
        cursor = mysql.connection.cursor()
        try:
            # Asegúrate de que los nombres de las columnas en la consulta coincidan con tu esquema de DB
            query = "INSERT INTO Book (titulo, autor, anio, genero, stock) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (titulo, autor, anio, genero, stock))
        except Exception as e:
            print("No se pudo registrar el libro:", e)
            flash("No se pudo registrar el libro.", "warning")
            return render_template("agregar-libros.html")
            
        
        mysql.connection.commit()
        cursor.close()
        
        # Flash book creation success
        flash(f"Libro creado correctamente.\nTítulo: {titulo}\nAutor: {autor}\nAño: {anio}\nGénero: {genero}\nStock: {stock}", "success")
        return render_template("agregar-libros.html")
    
    
if __name__ == "__main__":
    app.run(debug=True)
