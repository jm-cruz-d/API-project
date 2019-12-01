import sqlalchemy as db
import getpass
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
import pandas as pd
import json
import requests
from bson.json_util import dumps
from sqlalchemy.sql import text
import sqlalchemy as db
from bottle import route, run, template, get, post, request
import random

password = getpass.getpass("Insert your mysql root password: ")
engine = db.create_engine('mysql+pymysql://root:{}@localhost/otraoportunidad'.format(password))
print("Connected to server!")

#@route('/hello/<name>')
#def index(name):
#    return template('<b>Hello {{name}}</b>!', name=name)

@get('/Users/<idUser>')
def query(idUser=0):
    query = """
        SELECT * FROM messages WHERE users_idUser='{}'
    """.format(idUser)
    print("Running query")
    print(query)
    df = pd.read_sql_query(query, engine)
    new = df.to_json(orient='records')
    return json.dumps(new)


@post('/user/create/<name>')
def createUser(name):
    query = "INSERT INTO users (userName) VALUES ('{}')".format(name)
    with engine.connect() as con:
        try:
            con.execute(query)
            #Get Response
            id = con.fetchone()[0]
            print(f"value inserted: {id}")
        except:
            print("At least I tried")
    
    q = """
        SELECT * FROM users WHERE userName='{}'
    """.format(name)
    print("Running query")
    print(q)
    df = pd.read_sql_query(q, engine)
    new = df.to_json(orient='records')
    return json.dumps(new)

'''
### Para probar en el jupyter notebook
#import requests

#data = requests.get('http://localhost:8080/chiste').json()
#print(data["chiste"])
'''

run(host='localhost', port=8080)