from flask import Flask, request, jsonify
from models import db, departments, jobs, hired_employees
import csv
from config import Config
from sqlalchemy import func, extract

# Inicializa la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/upload/<table_name>', methods=['POST'])
def upload_csv(table_name):
    """
    Endpoint para subir datos desde un archivo CSV a una tabla específica.

    Args:
        table_name (str): El nombre de la tabla a la que se subirán los datos. 
                          Debe ser 'departments', 'jobs' o 'hired_employees'.

    Returns:
        str: Mensaje de éxito o error.
    """
    file = request.files['file']
    if not file:
        return "No file provided", 400

    if table_name not in ['departments', 'jobs', 'hired_employees']:
        return "Invalid table name", 400

    data = csv.reader(file.stream.decode('utf-8').splitlines())
    next(data)  # Omitir la fila de encabezado

    if table_name == 'departments':
        for row in data:
            db.session.add(departments(nombre=row[0]))
    elif table_name == 'jobs':
        for row in data:
            db.session.add(jobs(titulo=row[0]))
    elif table_name == 'hired_employees':
        for row in data:
            db.session.add(hired_employees(nombre=row[0], departments_id=row[1], jobs_id=row[2]))

    db.session.commit()
    return "Data uploaded successfully", 200

@app.route('/batch_insert', methods=['POST'])
def batch_insert():
    """
    Endpoint para insertar datos en lotes en una tabla específica.

    Args:
        table_name (str): El nombre de la tabla a la que se insertarán los datos. 
                          Debe ser 'departments', 'jobs' o 'hired_employees'.
        rows (list): Lista de diccionarios con los datos a insertar.

    Returns:
        str: Mensaje de éxito o error.
    """
    data = request.json
    table_name = data.get('table_name')
    rows = data.get('rows')

    if not table_name or not rows:
        return "Invalid request", 400

    if table_name not in ['departments', 'jobs', 'hired_employees']:
        return "Invalid table name", 400

    if len(rows) > 1000:
        return "Batch size exceeds limit", 400

    if table_name == 'departments':
        for row in rows:
            db.session.add(departments(nombre=row['nombre']))
    elif table_name == 'jobs':
        for row in rows:
            db.session.add(jobs(titulo=row['titulo']))
    elif table_name == 'hired_employees':
        for row in rows:
            db.session.add(hired_employees(nombre=row['nombre'], departments_id=row['departments_id'], jobs_id=row['jobs_id']))

    db.session.commit()
    return "Batch insert successful", 200

@app.route('/metrics/quarterly_hires', methods=['GET'])
def quarterly_hires():
    """
    Endpoint para obtener el número de empleados contratados por trimestre en 2021,
    agrupados por departamento y trabajo.

    Returns:
        json: Lista de diccionarios con los datos de contrataciones por trimestre.
    """
    results = db.session.query(
        departments.nombre.label('departments'),
        jobs.titulo.label('jobs'),
        func.sum(func.case([(extract('quarter', hired_employees.fecha_contratacion) == 1, 1)], else_=0)).label('Pregunta 1'),
        func.sum(func.case([(extract('quarter', hired_employees.fecha_contratacion) == 2, 1)], else_=0)).label('Pregunta 2'),
        func.sum(func.case([(extract('quarter', hired_employees.fecha_contratacion) == 3, 1)], else_=0)).label('Pregunta 3'),
        func.sum(func.case([(extract('quarter', hired_employees.fecha_contratacion) == 4, 1)], else_=0)).label('Pregunta 4')
    ).join(departments, hired_employees.departments_id == departments.id
    ).join(jobs, hired_employees.jobs_id == jobs.id
    ).filter(extract('year', hired_employees.fecha_contratacion) == 2021
    ).group_by(departments.nombre, jobs.titulo
    ).order_by(departments.nombre, jobs.titulo).all()

    return jsonify([{
        'departments': row.departments,
        'jobs': row.jobs,
        'Pregunta 1': row.Pregunta 1,
        'Pregunta 2': row.Pregunta 2,
        'Pregunta 3': row.Pregunta 3,
        'Pregunta 4': row.Pregunta 4
    } for row in results])

@app.route('/metrics/above_average_hires', methods=['GET'])
def above_average_hires():
    """
    Endpoint para obtener los departamentos que contrataron más empleados que el promedio en 2021.

    Returns:
        json: Lista de diccionarios con los departamentos y el número de empleados contratados.
    """
    subquery = db.session.query(
        hired_employees.departments_id,
        func.count(hired_employees.id).label('total_hires')
    ).filter(extract('year', hired_employees.fecha_contratacion) == 2021
    ).group_by(hired_employees.departments_id).subquery()

    avg_hires = db.session.query(func.avg(subquery.c.total_hires)).scalar()

    results = db.session.query(
        departments.id,
        departments.nombre.label('departments'),
        func.count(hired_employees.id).label('Contratado')
    ).join(hired_employees, hired_employees.departments_id == departments.id
    ).filter(extract('year', hired_employees.fecha_contratacion) == 2021
    ).group_by(departments.id, departments.nombre
    ).having(func.count(hired_employees.id) > avg_hires
    ).order_by(func.count(hired_employees.id).desc()).all()

    return jsonify([{
        'identificacion': row.id,
        'departments': row.departments,
        'Contratado': row.Contratado
    } for row in results])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)