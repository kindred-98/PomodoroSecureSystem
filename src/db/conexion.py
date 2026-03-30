"""
Módulo: conexion.py
Responsabilidad: Gestionar conexión a MongoDB Atlas y proporcionar cliente global.
"""

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
import os


class ConexionMongoDB:
    """Gestor de conexión a MongoDB Atlas."""
    
    _instancia = None
    _cliente = None
    _base_datos = None
    
    def __new__(cls):
        """Singleton: garantiza una única instancia."""
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia
    
    def conectar(self, uri: str = None):
        """
        Establece conexión a MongoDB Atlas.
        
        Args:
            uri (str, optional): URI de conexión. Si no se proporciona,
                                 intenta usar variable de entorno MONGODB_URI
        
        Raises:
            ConnectionFailure: Si no se puede conectar a MongoDB
            ValueError: Si no hay URI disponible
        """
        if self._cliente is not None:
            return  # Ya conectado
        
        if uri is None:
            # Intentar obtener de variable de entorno
            uri = os.getenv('MONGODB_URI')
        
        if uri is None:
            raise ValueError(
                "No hay URI de MongoDB. Proporciona 'uri' o configura MONGODB_URI"
            )
        
        try:
            self._cliente = MongoClient(uri, serverSelectionTimeoutMS=5000)
            # Verificar conexión
            self._cliente.admin.command('ping')
            print("✅ Conectado a MongoDB Atlas")
            # Seleccionar base de datos
            self._base_datos = self._cliente['pomodoreso_secure']
        except (ServerSelectionTimeoutError, ConnectionFailure) as e:
            raise ConnectionFailure(f"No se pudo conectar a MongoDB: {e}")
    
    def desconectar(self):
        """Cierra la conexión a MongoDB."""
        if self._cliente is not None:
            self._cliente.close()
            self._cliente = None
            self._base_datos = None
            print("✅ Desconectado de MongoDB")
    
    def obtener_base_datos(self):
        """
        Retorna la instancia de base de datos.
        
        Returns:
            Database: Instancia de base de datos MongoDB
            
        Raises:
            ConnectionFailure: Si no hay conexión activa
        """
        if self._base_datos is None:
            raise ConnectionFailure("No hay conexión a MongoDB. Llama a conectar() primero")
        return self._base_datos
    
    def obtener_coleccion(self, nombre_coleccion: str):
        """
        Retorna una colección de MongoDB.
        
        Args:
            nombre_coleccion (str): Nombre de la colección
        
        Returns:
            Collection: Instancia de colección MongoDB
        """
        bd = self.obtener_base_datos()
        return bd[nombre_coleccion]
    
    @staticmethod
    def obtener_instancia():
        """
        Obtiene la instancia singleton de ConexionMongoDB.
        
        Returns:
            ConexionMongoDB: Instancia global
        """
        return ConexionMongoDB()


# Instancia global
conexion_global = ConexionMongoDB()
