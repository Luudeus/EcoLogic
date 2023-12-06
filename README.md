# Instrucciones:
### Requerimientos
- Para instalar todas las librerías necesarias, usar `pip install -r requirements.txt`
### Cómo correr la página de forma local
- Usar `python -m flask run` para echar a correr flask
### Cómo ingresar las credenciales de la base de datos
1. Crea un archivo llamado `.env` en la carpeta raíz, es decir, en la misma donde se encuentra el archivo `app.py`
2. Escribir los datos de conexión de esta forma:
DB_HOST={host}
DB_USER={usuario}
DB_PASS={contraseña}
DB_NAME={nombre de la base de datos}

Imagen de ejemplo:
![database_connection](/database.PNG)