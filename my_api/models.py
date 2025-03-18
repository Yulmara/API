from flask_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy

# Inicializa la instancia de SQLAlchemy
db = SQLAlchemy()

class departments(db.Model):
    """
    Modelo para la tabla 'departments'.

    Atributos:
        id (int): Identificador único del departamento.
        nombre (str): Nombre del departamento.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

class jobs(db.Model):
    """
    Modelo para la tabla 'jobs'.

    Atributos:
        id (int): Identificador único del trabajo.
        titulo (str): Título del trabajo.
    """
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)

class hired_employees(db.Model):
    """
    Modelo para la tabla 'hired_employees'.

    Atributos:
        id (int): Identificador único del empleado contratado.
        nombre (str): Nombre del empleado.
        departments_id (int): Identificador del departamento al que pertenece el empleado.
        jobs_id (int): Identificador del trabajo que tiene el empleado.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    departments_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    jobs_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)