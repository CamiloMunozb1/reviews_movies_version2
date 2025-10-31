# Importacion de librerias necesarias y Blueprints para el uso de la funcionalidad en la aplicacion principal.
from flask import Blueprint,request,jsonify
from backend.data import conexion
from dotenv import load_dotenv
import requests
import psycopg2
import os

# Ingreso del Blueprint hacia la aplicacion.
eliminar_review = Blueprint('delete_review',__name__)

load_dotenv() # Importacion de las variables de entorno.

# Conexion con la base de datos.
def conexion_db():
    return conexion.conexion_db()

def eliminacion_notion(notion_page_id):
    api_key = os.getenv('API_KEY')
    database = os.getenv('ID_DATABASE')
    url = f'https://api.notion.com/v1/pages/{notion_page_id}'

    if not api_key or not database:
        print('No se encontro la conexion con la nube de Notion.')
    
    try:
            headers = {
                'Authorization' : f'Bearer{api_key}',
                'Content-Type' : 'application/json',
                'Notion-Version' : '2025-09-03'
            }

            data = {
                'archived' : True
            }
            respuesta = requests.post(url=url,headers=headers,json=data)
            if respuesta.status_code == 200:
                print('Review de la pagina eliminado con exito.')
            else:
                print(f'Error en la eliminacion de la review : {respuesta.status_code}, {respuesta.text}.')
    except Exception as error:
        print(f'Error en la subida de la informacion a la nube : {error}.')
    

# Routa de la aplicacion modular con el metodo 'POST'
@eliminar_review.route('/delete',methods = ['POST'])
def delete_movie():
    data = request.get_json() # Se ingresa la informacion en formato Json.

    try:
        movie_id = int(data.get('movie_id','')) # Se usa el ID para hacer una eliminacion completa de los campos ingresados.
    except ValueError:
        return jsonify({'Error' : 'error de digitacion en el campo.'})

    if not movie_id: # Validador de campo donde se debe tener el campo completo.
        return jsonify({'Error' : 'todos los campos deben estar completos.'}),400
    

    conn = conexion_db() # Uso de la conexion con la base de aatos y validador de conexion.
    if conn is None:
        return jsonify({'Error' : 'no se encontro la conexion con la base de datos.'}),400
    
    try:
        cursor = conn.cursor() # Cursor para el uso y manejo de la base de datos.
        # Primero, encapsulamos el id de la pagina de notion para usarlo en la nube.
        cursor.execute('''SELECT notion_page_id FROM reviews_movie WHERE movie_id = %s''',(movie_id,))
        notion_page = cursor.fetchone() # Buscamos el id geneado de la pagina.
        if not notion_page:
            return jsonify({'Error' : f'no se encontro el id de la pagina de Notion: {notion_page}.'}),404
        notion_page_id = notion_page[0] # Encapsulamiento del id.
        notion_delete = eliminacion_notion(notion_page_id) # Se pasa el ID a la API.
        if notion_delete:
            return jsonify({'Error' : f'fallo en la integracion con la nube: {notion_delete}'}),502
        cursor.execute('''DELETE FROM reviews_movie WHERE movie_id = %s''',(movie_id,)) # Consulta para la eliminacion del campo en la base de datos.
        if cursor.rowcount == 0: # Rastreo del ID de la base de datos.
            conn.rollback()
            return jsonify({'Error' : 'no se encontro el id de la review.'}),400
        conn.commit() # Subida de informacion a la base de datos.
        return jsonify({'Mensaje' : 'Review eliminada con exito.'}),200
    # Manejo de errores.
    except psycopg2.errors.IntegrityError:
        conn.rollback() # Elimina los cambios subidos.
        return jsonify({'Error' : 'error de integridad en la base de datos.'}),400
    except Exception as error:
        return jsonify({'Error' : f'error en el programa : {error}.'})
    finally:
        cursor.close() # Cierre del cursor.
        conn.close() # Cierre de la conexion.



