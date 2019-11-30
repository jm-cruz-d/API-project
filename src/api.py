import sqlalchemy as db
import getpass
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
import pandas as pd
import json
from sqlalchemy.sql import text
import sqlalchemy as db
from bottle import route, run, template, get, post
import random

password = getpass.getpass("Insert your mysql root password: ")
engine = db.create_engine('mysql+pymysql://root:{}@localhost/conversation'.format(password))
print("Connected to server!")

#@route('/hello/<name>')
#def index(name):
#    return template('<b>Hello {{name}}</b>!', name=name)

@get('/')
def index():
    query = """
        SELECT * FROM conversation.messages
    """
    df = json.dumps(query, engine)
    return df



run(host='localhost', port=8080)


### Para probar en el jupyter notebook
import requests

data = requests.get('http://localhost:8080/chiste').json()
print(data["chiste"])