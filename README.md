# Instrucciones:
### Requerimientos
- Para instalar todas las librerías necesarias, una vez en el directorio del proyecto, usar `pip install -r requirements.txt`
- Para la base de datos, abrir el archivo [SGDB_script.sql](/SGDB_script.sql) en MySQL Workbench, y luego darle al rayo.
### Cómo correr la página de forma local
- Usar `python -m flask run` para echar a correr flask
### Cómo ingresar las credenciales de la base de datos
1. Crea un archivo llamado `.env` en la carpeta raíz, es decir, en la misma donde se encuentra el archivo `app.py`
2. Escribir los datos de conexión de esta forma:<br>
DB_HOST={host}<br>
DB_USER={usuario}<br>
DB_PASS={contraseña}<br>
DB_NAME={nombre de la base de datos}<br>

**Imagen de ejemplo:**<br>
![database_connection](/database.PNG)
