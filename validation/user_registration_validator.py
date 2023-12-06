import re
from werkzeug.security import generate_password_hash


def validate_user_input(rut=None, name=None, mail=None, password=None, confirmation=None):
    """Validate user input for registration.

    Args:
        rut (str, optional): The user's RUT.
        name (str, optional): The user's name.
        mail (str, optional): The user's email.
        password (str, optional): The user's password.
        confirmation (str, optional): The password confirmation.

    Returns:
        list: A list of error messages, if any.

    """
    errors = []

    # Basic validations
    if not rut:
        errors.append("Se debe ingresar el RUT")
    if not name:
        errors.append("Se debe ingresar el nombre")
    if not mail:
        errors.append("Se debe ingresar el correo")
    if not password:
        errors.append("Se debe ingresar la contraseña")
    if not confirmation:
        errors.append("Se debe re-ingresar la contraseña")

    # Check if passwords match
    if password != confirmation:
        errors.append("La contraseña y la contraseña de confirmación no coinciden")

    # Password complexity validation
    if not is_password_complex(password):
        errors.append("La contraseña debe contener al menos 3 letras y 2 dígitos")

    return errors


def is_password_complex(password):
    """Check if the password meets complexity requirements.

    Args:
        password (str): The user's password.

    Returns:
        bool: True if the password meets complexity requirements, False otherwise.

    """
    digits = re.findall(r"\d", password)
    letters = re.findall(r"[A-Za-z]", password)
    return len(digits) >= 2 and len(letters) >= 3


def hash_password(password):
    """Generate a password hash.

    Args:
        password (str): The user's password.

    Returns:
        str: The hashed password.

    """
    return generate_password_hash(password)
