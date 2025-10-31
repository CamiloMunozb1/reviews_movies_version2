# Librerias necesarias para uso del framework, carga de variables de entorno, bases de datos y manejo del sistema.
from flask import Flask,jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
import os

# Constructor de una aplicacion Flask.
app = Flask(__name__)
CORS(app,origins='www.paginadejemplo.com',supports_credentials=True) # Conexion hacia el fronted.
load_dotenv() # Carga de las variables de entorno

def conexion_db():
    try:
        # Conexion con la base de datos.
        conn = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            dbname = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            port = os.getenv('DB_PORT'),
            sslmode = os.getenv('DB_SSL')
        )
        return conn # Retorno de la conexion.
    # Manejo de errores.
    except psycopg2.errors.InternalError:
        return jsonify({'Error' : 'error interno en la conexion con la base de datos.'}),400
    except Exception as error:
        print(f'Error inesperado en el programa : {error}.')
    finally:
        conn.close() # Cierre de la conexion.
