# Importacion de las kibrerias necesarias y pandas para visualizar los datos.
from flask import Blueprint,jsonify
from backend.data import conexion
from dotenv import load_dotenv
import psycopg2
import pandas as pd

# Ingreso del blueprint hacia la aplicacion.
show_reviews = Blueprint('show_reviews',__name__)
load_dotenv() # Carga de variables de entorno.
# Conexion con la base de datos.
def conexion_db():
    return conexion.conexion_db()

# Routa de la aplicacion modular con el metodo 'GET'
@show_reviews.route('/show',methods=['GET'])
def show_reviews():
    try:
        conn = conexion_db() # Conexion con la base de datos y campo de verificacion de conexion.
        if conn is None:
            return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'}),400
        # Leida de la consulta para mostrar los datos de cada campo.
        df = pd.read_sql_query('''SELECT * FROM reviews_movie''',conn)
        resultado = df.to_dict(['records']) # Se muestran los datos en formato Json.
        if not resultado:
            return jsonify({'Mensaje' : resultado}),200 # Muestra el resultado.
        else:
            return jsonify({'Mensaje' : 'no se encontraron registros.'}),200 # Si no se encuentran datos se usa el else.
    # Manejo de errores.
    except psycopg2.errors.IntegrityError:
        return jsonify({'Error' : 'error de integridad en la base de datos.'}),400
    except Exception as error:
        print(f'Error en la aplicacion: {error}'),400
    finally:
        conn.close() # Cierre de la conexion.
