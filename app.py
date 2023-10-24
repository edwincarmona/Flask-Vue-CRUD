from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.mysql import MySQL  # pip install flask-mysql
import pymysql

MEMBERS = [
    {
        'id': '1',
        'firstname': 'cairocoders',
        'lastname': 'Ednalan',
        'address': 'Olongapo City'
    },
    {
        'id': '2',
        'firstname': 'cairocoders',
        'lastname': 'Ednalan',
        'address': 'Olongapo City'
    }
]

# Configuration
DEBUG = True

# Instanciar app
app = Flask(__name__)
app.config.from_object(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'msroot'
app.config['MYSQL_DATABASE_DB'] = 'py_test_crud'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# habilitar CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Ruta para prueba del service de Flask
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

# Ruta ejemplo de obtención de JSON
@app.route('/members', methods=['GET'])
def all_members():
    return jsonify({
        'status': 'success',
        'members': MEMBERS
    })

# Ruta Home
@app.route('/')
def home():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM members ORDER BY id ASC")
        userslist = cursor.fetchall()
        return jsonify({
            'status': 'success',
            'members': userslist
        })
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# Método INSERT, recibe parámetros de registro miembro
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        message = ""
        
        try:
            post_data = request.get_json(silent=True)
            firstname = post_data.get('firstname')
            lastname = post_data.get('lastname')
            address = post_data.get('address')

            sql = "INSERT INTO members(firstname, lastname, address) VALUES (%s, %s, %s)"
            data = (firstname, lastname, address)
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql, data)
            conn.commit()
            message = "Successfully Added"
        except Exception as e:
            print(e)
            message = str(e)
        finally:
            cursor.close()
            conn.close()

        response_object['message'] = message
    return jsonify(response_object)

# Editar registro
@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    response_object = {'status': 'success'}
    row = {}
    message = ""
    
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM members WHERE id = %s", [id])
        row = cursor.fetchone()
    except Exception as e:
        print(e)
        message = str(e)
    finally:
        cursor.close()
        conn.close()

    response_object['message'] = message
    response_object['editmember'] = row
    return jsonify(response_object)

# Actualizar registro
@app.route('/update', methods=['PUT'])
def update():
    response_object = {'status': 'success'}
    message = ""
    
    try:
        put_data = request.get_json(silent=True)
        firstname = put_data.get('firstname')
        lastname = put_data.get('lastname')
        address = put_data.get('address')
        id_member = put_data.get('id')

        sql = "UPDATE members SET firstname = %s, lastname = %s, address = %s WHERE id = %s"
        data = (firstname, lastname, address, id_member)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, data)
        conn.commit()
        message = "Successfully modified"
    except Exception as e:
        print(e)
        message = str(e)
    finally:
        cursor.close()
        conn.close()

    response_object['message'] = message
    return jsonify(response_object)

# Eliminar registro
@app.route('/delete/<string:id>', methods=['DELETE'])
def delete(id):
    response_object = {'status': 'success'}
    message = ""
    
    try:
        sql = "DELETE FROM members WHERE id = %s"
        data = (id)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, data)
        conn.commit()
        message = "Successfully deleted"
    except Exception as e:
        print(e)
        message = str(e)
    finally:
        cursor.close()
        conn.close()

    response_object['message'] = message
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
