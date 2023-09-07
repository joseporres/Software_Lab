from flask import Flask, request, jsonify
import mysql.connector
import os

application = Flask(__name__)

# Configura la conexión a la base de datos MySQL
def get_connection():
    if 'RDS_HOSTNAME' in os.environ:
        DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', 'NAME': os.environ['RDS_DB_NAME'], 'USER': os.environ[
            'RDS_USERNAME'], 'PASSWORD': os.environ['RDS_PASSWORD'], 'HOST': os.environ['RDS_HOSTNAME'], 'PORT': os.environ['RDS_PORT'], }}
        dbname = os.environ['RDS_DB_NAME']
        dbuser = os.environ['RDS_USERNAME']
        dbpwd = os.environ['RDS_PASSWORD']
        dbport = os.environ['RDS_PORT']
        dbhost = os.environ['RDS_HOSTNAME']
        connection = mysql.connector.connect(
            host=dbhost, database=dbname, user=dbuser, password=dbpwd)
        return connection
    else:
        return None

# Index
@application.route('/')
def index():
    db = get_connection()
    cursor = db.cursor()
    return "Bienvenido a la API de transferencias esta conectado a la base de datos"

# Endpoint para obtener todos los usuarios
@application.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return jsonify(usuarios)


# Endpoint para crear la tabla
@application.route('/creartabla', methods=['POST'])
def crear_tabla():
    db = get_connection()
    cursor = db.cursor()
    tabla_sql = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario VARCHAR(255) NOT NULL,
        saldo DECIMAL(10, 2)
    )
    """
    cursor.execute(tabla_sql)
    db.commit()
    return "Tabla creada exitosamente"

# Endpoint para crear un usuario con saldo inicial
@application.route('/crearusuario/<usuario>', methods=['POST'])
def crear_usuario(usuario):
    db = get_connection()
    cursor = db.cursor()
    saldo_inicial = 100.0
    insert_sql = "INSERT INTO usuarios (usuario, saldo) VALUES (%s, %s)"
    cursor.execute(insert_sql, (usuario, saldo_inicial))
    db.commit()
    return f"Usuario '{usuario}' creado con un saldo inicial de {saldo_inicial}"

# Endpoint para transferir saldo entre usuarios
# url: transferir/<usuario1>?destino=<usuario2>&valor=<valor>
@application.route('/transferir/<usuario1>', methods=['POST'])
def transferir(usuario1):
    db = get_connection()
    cursor = db.cursor()
    destino = request.args.get('destino')
    valor = float(request.args.get('valor'))

    # Verificar si el usuario1 tiene saldo suficiente para la transferencia
    cursor.execute("SELECT saldo FROM usuarios WHERE usuario = %s", (usuario1,))
    saldo_usuario1 = cursor.fetchone()

    if saldo_usuario1 is None:
        return f"El usuario '{usuario1}' no existe"

    saldo_usuario1 = saldo_usuario1[0]

    if saldo_usuario1 < valor:
        return "Saldo insuficiente para la transferencia"

    #Realizar la transferencia
    cursor.execute("UPDATE usuarios SET saldo = saldo - %s WHERE usuario = %s", (valor, usuario1))
    cursor.execute("UPDATE usuarios SET saldo = saldo + %s WHERE usuario = %s", (valor, destino))
    db.commit()
    
    return f"Transferencia de {valor} de '{usuario1}' a '{destino}' realizada con éxito"

if __name__ == '__main__':
    application.run(debug=True)
