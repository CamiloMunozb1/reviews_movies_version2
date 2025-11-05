## 🎥 Movie Review Sync Backend (Flask + PostgreSQL + Notion)

Este proyecto es un backend RESTful desarrollado con Flask para gestionar reseñas de películas. La aplicación garantiza la atomicidad de las operaciones: cada reseña se guarda en una base de datos local (PostgreSQL) y se sincroniza automáticamente con una base de datos en Notion, asegurando que ambas fuentes de datos permanezcan consistentes.

## ✨ Características Principales

-API REST con Flask:  Rutas para crear y eliminar reseñas.
-Conexión a PostgreSQL: Persistencia de datos local.
-Sincronización con Notion: Integración con la API de Notion para mantener una copia de las reseñas en la nube.
-Transacciones Atómicas: Uso de commit y rollback para asegurar que las operaciones (DB local + Notion) sean exitosas o ninguna lo sea.

## 🛠️ RequisitosPara ejecutar este proyecto, necesitas tener instalados:

-Python 3.x
-PostgreSQL (y acceso a una base de datos)
-Acceso a la API de Notion (un token de integración y un ID de base de datos)
-Dependencias de PythonLas principales librerías utilizadas se pueden instalar con pip:
            pip install Flask flask-cors psycopg2-binary python-dotenv requests
            
## ⚙️ Configuración del Entorno

La aplicación utiliza variables de entorno para manejar las credenciales y la configuración de las APIs y la base de datos. Debes crear un archivo llamado .env en la raíz del proyecto.Archivo .env 
        # ------------------------------------
        # CONFIGURACIÓN DE POSTGRESQL
        # ------------------------------------
        DB_HOST=localhost
        DB_NAME=mis_peliculas
        DB_USER=postgres
        DB_PASSWORD=mysecretpassword
        DB_PORT=5432
      
        # ------------------------------------
        # CONFIGURACIÓN DE NOTION API
        # ------------------------------------
        # El Token de Integración de la API de Notion
        API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxx 
        # El ID de la base de datos de Notion donde se guardarán las reseñas
        ID_DATA_BASE=xxxxxxxxxxyxxxxxxxxxxxxxxxxxxxx
    
## 🚀 Uso y Endpoints

El servidor se ejecuta con un comando básico de Flask (asumiendo que tu archivo principal se llama app.py).
Endpoints Disponibles
1. Crear Nueva Reseña (Atomicidad: DB INSERT + NOTION INSERT)
2. Ruta: /moviesMétodo: POST
3. Cuerpo (JSON Requerido):
           {
            "pelicula_name": "Interestellar",
            "reseña_pelicula": "Una obra maestra de ciencia ficción...",
            "calificacion_usario": 5
          }
5. Eliminar Reseña (Atomicidad: DB DELETE + NOTION ARCHIVE)
6. Ruta: /movies/delete (Asumiendo que es parte de tu Blueprint eliminar_review)
7. Método: POSTCuerpo (JSON Requerido):
         {
          "movie_id": 42
       }
(Nota: El movie_id debe ser el ID primario de la reseña en tu base de datos PostgreSQL).

## ⚠️ Coherencia de Datos (Importante)La clave de este backend es la coherencia. 

Para que la eliminación funcione, tu tabla reviews_movie en PostgreSQL DEBE guardar el ID de la página de Notion (notion_page_id) que se recibe cuando se crea la reseña.

## Autor

Proyecto realizado por Juan Camilo Muñoz 

## Licencia

Este proyecto esta bajo una licencia MIT.
