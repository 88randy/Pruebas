import json
import sqlite3
from flask import Flask, render_template


def get_db_connection():
    conn = sqlite3.connect('sitio.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/proyecto/<int:id>', methods = ['GET'])
def index(id):
    # Inicializamos los arreglos
    proyectos = []
    usuarios = []
    
    # Creamos la conexión a la base de datos
    conn = get_db_connection()
    
    """
    # Hacemos la consulta con el id proporcionado por el cliente
    query_projects_id = conn.execute(f'''SELECT id, project_name FROM project WHERE id = {id}''').fetchone()

    # Buscamos todos los datos que sean iguales a project_name
    query_projects = conn.execute(f'''SELECT id, 
                                        project_images, 
                                        project_description, 
                                        project_name,
                                        project_active 
                                    FROM project
                                    WHERE project_name = "{query_projects_id[1]}"''').fetchall()
    """
    
    # Hacemos las consultas a la base de datos
    query_projects = conn.execute(f'''SELECT id, 
                                        project_images, 
                                        project_description, 
                                        project_name,
                                        project_active 
                                    FROM project
                                    WHERE id = {id}''').fetchall()
    
    query_users = conn.execute('''SELECT us.id, 
                                        us.username, 
                                        us.password, 
                                        us.profile_picture, 
                                        us.user_full_name, 
                                        ro.id role_id, 
                                        ro.name, 
                                        ro.description
                                    FROM user AS us
                                    JOIN user_role_association_table AS ur
                                    ON us.id = ur.user_id
                                    JOIN role AS ro
                                    ON ur.role_id = ro.id''').fetchall()
    # Cerramos la conexión a la base de datos
    conn.close()
    
    # Guardamos la información en los arreglos
    if not query_projects:
        proyectos.append({'Not Found': '404'})
    else:
        for row in query_projects:
            proyectos.append({'id': row[0], 
                            'project_images': row[1], 
                            'project_description': row[2], 
                            'project_name':row[3],
                            'project_active': row[4]})
    for row in query_users:
        usuarios.append({'id': row[0], 
                        'username': row[1], 
                        'password': row[2], 
                        'profile_picture':row[3],
                        'user_full_name': row[4],
                        'role_id': row[5],
                        'name': row[6],
                        'description': row[7]})
    
    # Creamos el objeto data con los arreglos proyectos y usuarios
    data = {"projects": proyectos, "user":usuarios}
    
    # Convertimos el objeto a JSON
    objects = json.dumps(data, indent = 4, default = str, sort_keys = True)
    
    # Enviamos al navegador del cliente
    return render_template('index.html', objects = objects)