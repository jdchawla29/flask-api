import json
from typing import OrderedDict
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'data'

mysql = MySQL(app)

def returnIds(data):
    lst = data.decode().strip().split()
    ids = tuple([int(id) for id in lst])
    return ids

def executeQuery(ids):
    cursor = mysql.connection.cursor()
    format_strings = ','.join(['%s'] * len(ids))
    cursor.execute("SELECT * FROM data_table WHERE id IN (%s)" % format_strings,ids)
    rows = cursor.fetchall()
    return rows

@app.route('/', methods=['POST'])
def index():
    ids = returnIds(request.data)
    rows = executeQuery(ids)

    try:
        response = OrderedDict(rows)
        return json.dumps(response),200
    except:
        return json.dumps({"error":"not found"}), 404

if __name__ == '__main__':
    app.run()
