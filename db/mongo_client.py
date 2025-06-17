import os
from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv

load_dotenv(".env")

class MongoConnection:
    """
    Una clase Singleton para gestionar la conexión a MongoDB.
    """
    __instance = None
    __client = None
    __db = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(MongoConnection, cls).__new__(cls)
            try:
                mongo_uri = os.getenv("MONGO_URI")
                mongo_user = os.getenv("MONGO_USERNAME")
                mongo_password = os.getenv("MONGO_PASSWORD")
                mongo_auth_source = os.getenv("MONGO_AUTH_SOURCE", "admin")
                db_name = os.getenv("DB_NAME", "main_db")

                cls.__client = MongoClient(
                    host=mongo_uri,
                    username=mongo_user,
                    password=mongo_password,
                    authSource=mongo_auth_source,
                    authMechanism="SCRAM-SHA-256"
                )
                cls.__db = cls.__client[db_name]
                print("✅ Conexión a MongoDB establecida.")
            except Exception as e:
                print(f"❌ Error al conectar a MongoDB: {e}")
                cls.__instance = None
        return cls.__instance

    def get_collection(self, collection_name: str) -> Collection:
        """
        Obtiene una colección de la base de datos.
        """
        if self.__db is not None:
            return self.__db[collection_name]
        raise Exception("La conexión a la base de datos no está establecida.")
    
    def get_db(self):
        """
        Obtiene la instancia de la base de datos.
        """
        if self.__db is not None:
            return self.__db
        raise Exception("La conexión a la base de datos no está establecida.")




# Instancia global para ser importada por otros módulos
db_connection = MongoConnection()