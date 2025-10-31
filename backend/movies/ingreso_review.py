# Importacion de las librerias necesarias y funcionalidades modulares de la aplicacion.
from flask import Flask, request, jsonify
from backend.data import conexion
from backend.movies import eliminar_review
from backend.movies import mostrar_review
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
import requests
import os

# Constructor de la aplicacion.
app = Flask(__name__)
CORS(app,origins='www.paginadeejemplo.com',supports_credentials=True) # Comexion con el fronted.

# Uso de la conexion establecida con la base de datos.
def conexion_db():
        return conexion.conexion_db()

# Aplicaciones modulares.
app.register_blueprint(eliminar_review)
app.register_blueprint(mostrar_review)

load_dotenv() # Carga de variables de entorno.


# Ingreso de una funcion auxiliar.
def ingreso_nube(nombre,reseña,calificacion): # Ingreso de la informacion de la aplicacion principal.

        # Ingreso del id de la base de datos y la api key para la conexion con la nube de Notion.
        data_id = os.getenv('id_data_base')
        api_key = os.getenv('API_KEY')
        url = 'https://api.notion.com/v1/pages' # URL para la conexion con la nube de Notion.

        # Campo de Validacion de credenciales.
        if not data_id or not api_key:
                print('No se encuentra la conexion con la nube de notion.')
        try:
                headers = {
                        'Authorization' : f'Bearer {api_key}', # Autorizacion de la api key.
                        'Content-type' : 'application/json', # Contenido tipo Json.
                        'Notion-Version' : '2025-09-03' # Version de la API.
                }
                
                # Data se encarga de la subida de la informacion a la nube de Notion.
                data = {
                        'parent' : {'database_id' : data_id}, # Conexion con la base de datos en la nube.
                        'propierties' : {
                                # Se ingresan las propiedades a la nube de Notion.
                                'pelicula_name' : {
                                        'title' : [{
                                                'text' : {'content' : nombre}
                                        }]
                                },
                                'reseña_usuario' : {
                                        'richt_text' : [{
                                                'text' : {'content' : reseña}
                                        }]
                                },
                                'calificacion_usuario' : {
                                        'number' : calificacion
                                }
                        }
                }
                # En la respuesta se pasa los parametros establecidos anteriormente y a donde se van a pasar.
                respuesta = requests.post(url=url,headers=headers,json=data)
                if respuesta.status_code == 200: # Si la respuesta es 200 se sube la informacion
                        print('La informacion se subio con exito a la nube.')
                else:
                        print(f'Error: {respuesta.status_code},{respuesta.text}')
        except Exception as error:
                print(f'Error con la subida de la informacion a la nube : {error}.')


# Enrutador principal de la aplicacion con el metodo POST.
@app.route('/movies',methods = ['POST'])
def ingreso_peliculas():
        data = request.get_json() # Se ingresa la informacion en formato Json.

        try:
                # Campos de ingreso del usuario.
                pelicula_name = data.get('pelicula_name','').strip()
                reseña_pelicula = data.get('reseña_pelicula','').strip()
                calificacion_usuario = int(data.get('calificacion_usario',''))
        except ValueError:
                print('Error en la digitacion de los datos, volver a intentar.')

        # Campo de verificacion de campo.
        if all([pelicula_name,reseña_pelicula,calificacion_usuario]):
                return jsonify({'Error' : 'todos los campos deben estar completos.'}),400
        
        # Se integra la conexion con la base de datos y se verifica que la conexion este disponible.
        conn = conexion_db()
        if conn is None:
                return jsonify({'Error' : 'No se encontro la conexion con la base de datos.'}),400
        
        try:
                cursor = conn.cursor() # Cursor para uso de consultas hacia la base de datos.
                # Se hace la consulta para subir la informacion a la base de datos.
                cursor.execute('''
                                INSERT INTO reviews_movie(pelicula_name,reseña_pelicula,calificacion_usuario) 
                                VALUES (%s,%s,%s) 
                                RETURNING id_movie'''
                                (pelicula_name,reseña_pelicula,calificacion_usuario)
                        )
                # Retorno del ID generado.
                movie_id =  cursor.fetchone[0]
                conn.commit() # Subida de datos a la base de datos.
                notion_integration = ingreso_nube(pelicula_name,reseña_pelicula,calificacion_usuario) # Retorno de las variables de ingreso para la API.
                # Comprobacion de subida a la API.
                if notion_integration:
                        conn.rollback() # Deteccion de error para evitar subida a las dos bases de datos.
                        return jsonify({'Mensaje' : f'fallo la integracion con la nube: {notion_integration}.'})
                return jsonify({'Mensaje' : 'reseña de pelicula añadida con exito', 'movie_id' : movie_id}),200
        # Manjeo de erroes.
        except psycopg2.errors.IntegrityError:
                conn.rollback() # Si se detecta un error se eliminan los cambios.
                return jsonify({'Error' : 'error de integridad en la base de datos.'}),400
        except Exception as error:
                return jsonify({'Error' : f'error inesperado en el programa : {error}.'})
        finally:
                cursor.close() # Cierre del cursor,
                conn.close() # Cierre de la conexion.
