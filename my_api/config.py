import os

class Config:
    """
    Clase de configuración para la aplicación Flask.

    Atributos:
        SQLALCHEMY_DATABASE_URI (str): URI de la base de datos SQLAlchemy.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Desactiva el seguimiento de modificaciones de SQLAlchemy.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mydatabase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False