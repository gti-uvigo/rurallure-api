import os
from db.mongo_client import db_connection
from gridfs import GridFS
from flask import Response


def get_method(collection_name: str, filter: dict, many: bool = False):
    """
    Obtiene uno o varios documentos de la colección especificada que coincidan con el filtro dado.

    :param collection_name: Nombre de la colección en la base de datos.
    :param filter: Filtro para buscar el/los documento(s).
    :param many: Si es True, devuelve una lista de documentos; si es False, devuelve un solo documento.
    :return: Documento encontrado, lista de documentos, o None si no se encuentra.
    """
    collection = db_connection.get_collection(collection_name)
    if many:
        return list(collection.find(filter))
    else:
        return collection.find_one(filter)
    

    
def post_method(collection_name: str, document: dict):
    """
    Inserta un nuevo documento en la colección especificada.

    :param collection_name: Nombre de la colección en la base de datos.
    :param document: Documento a insertar.
    :return: ID del documento insertado.
    """
    collection = db_connection.get_collection(collection_name)
    result = collection.insert_one(document)
    return str(result.inserted_id)
    
def update_method(collection_name: str, filter: dict, update: dict):
    """
    Actualiza un documento en la colección especificada que coincida con el filtro dado.

    :param collection_name: Nombre de la colección en la base de datos.
    :param filter: Filtro para buscar el documento a actualizar.
    :param update: Datos de actualización.
    :return: Resultado de la operación de actualización.
    """
    collection = db_connection.get_collection(collection_name)
    result = collection.update_one(filter, update)
    return result.modified_count

 
def get_image_gridfs(image_id):
    """
    Descarga una imagen almacenada en GridFS.

    :param file_id: ID del archivo a descargar.
    :param collection_name: Nombre de la colección de GridFS (por defecto es "images").
    :return: Contenido del archivo descargado.
    """
    fs = GridFS(db_connection.get_db())
    
    try:
        file_data = fs.find_one({"image_id": image_id})
        response = Response(file_data.read(), mimetype=file_data.content_type)
        response.headers['Content-Length'] = str(file_data.length)
        return response
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        return None
    


def upload_image_gridfs(image, image_id=None, metadatos=None):
    """
    Sube una imagen a GridFS.
    :param image: Archivo de imagen a subir.
    :param image_id: ID personalizado para la imagen (opcional).
    :param metadatos: Diccionario de metadatos adicionales para la imagen (opcional).
    :return: ID del archivo subido o None si hubo un error.
    """
    fs = GridFS(db_connection.get_db())

    try:
        file_id = fs.put(image, filename=image_id+".jpg", image_id=image_id, **(metadatos or {}))
        return file_id
    except Exception as e:
        print(f"Error al subir la imagen '{image_id}' a GridFS: {e}")
        return None
    