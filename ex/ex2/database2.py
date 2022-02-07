import sqlite3
from flask import Flask, render_template,request


app = Flask(__name__)
delta = 0
@app.route('/ex2')
def index():
    conn = sqlite3.connect( app.root_path+'/database/chinook.db') 
    
    qtables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table = None
    if 'table' in request.args.keys():
        table = request.args['table']
    else:
        table = qtables[0][0]
    if 'page' in request.args.keys():
        num = int(request.args['page'])
    else: num = 1
    tableq = conn.execute(f"SELECT * FROM {table} LIMIT {(int(num)-1)*10}, 10")
    dep =[ i[0] for i in  tableq.description]
    data = tableq.fetchall()

    #SELECT COUNT(*) FROM playlists 
    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    maxNum = (count // 10)+1

    navList = []
    if maxNum <= 10:
        navList = [i for i in range(1,maxNum+1) ]
    else:
        # << 1 2 3 4 5 6 7 8 9 10 >>
        if num <=8 :
            navList = [i for i in range(1,11) ]
        elif num >= maxNum-7:
            navList = [i for i in range(maxNum-9,maxNum+1) ]
        else:
            navList = [i for i in range(num-5,num+6) ]

    
    conn.close()
    return render_template('index.html', colnames=dep,data=data,table = table,tables=[i[0] for i in qtables],maxNum= maxNum,nav = navList,num = num)

