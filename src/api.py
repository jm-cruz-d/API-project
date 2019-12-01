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

# Select messages from idUser
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

'''
FUNCIÓN METIENDOLO EN LA URL
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

# Create a User in Database
@post('/user/create')
def createUser():
    name = str(request.forms.get('name'))
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

# Create a Chat in Database
@post('/chat/create')
def createChat():
    with engine.connect() as con:
        number_chat = list(con.execute("SELECT idChat FROM chats ORDER BY idChat DESC LIMIT 1"))
        new_chatId = number_chat[0][0]+1
    with engine.connect() as con:
        query = "INSERT INTO chats (idChat) VALUES ({})".format(new_chatId)
        con.execute(query)
    return {f'{new_chatId}': 'Created chat'}

# Create a Message in Database
@post('/chat/<chat_id>/addmessage')
def createMessage(chat_id):
    text = str(request.forms.get('text'))
    user = int(request.forms.get('user_id'))
    chat = chat_id
    query = '''INSERT INTO messages (text, datetime, users_idUser, chats_idChat) VALUES ('{}', CURRENT_TIMESTAMP, {}, {})'''.format(text, user, chat)
    with engine.connect() as con:
            con.execute(query)
    
    q = """
        SELECT idMessage FROM messages WHERE text='{}'
    """.format(text)
    print("Running query")
    print(q)
    df = pd.read_sql_query(q, engine)
    new = df.to_json(orient='records')
    return json.dumps(new)

# Select text from a chat
@get('/chat/<chat_id>/list')
def queryMessages(chat_id):
    query = """
        SELECT text FROM messages WHERE chats_idChat='{}'
    """.format(chat_id)
    print("Running query")
    print(query)
    df = pd.read_sql_query(query, engine)
    new = df.to_json(orient='records')
    return json.dumps(new)


'''
### Para probar en el jupyter notebook
#import requests

#data = requests.get('http://localhost:8080/chiste').json()
#print(data["chiste"])
'''

run(host='localhost', port=8080)