import sqlite3
from flask import Flask, render_template,request


app = Flask(__name__)

@app.route('/ex1')
def index():
    conn = sqlite3.connect(app.root_path+'/database/chinook.db') 
    qtables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table = None
    if 'table' in request.args.keys():
        table = request.args['table']
    else:
        table = qtables[0][0]

    tableq = conn.execute(f"SELECT * FROM {table}")

    dep =[ i[0] for i in  tableq.description]
    data = tableq.fetchall()
    conn.close()
    return render_template('index.html', colnames=dep,data=data,tables=[(i[0],table == i[0]) for i in qtables])

