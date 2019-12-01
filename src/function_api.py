import sqlalchemy as db
import getpass
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
import pandas as pd
import json
from sqlalchemy.sql import text
import sqlalchemy as db

password = getpass.getpass("Insert your mysql root password: ")
engine = db.create_engine('mysql+pymysql://root:{}@localhost/otraoportunidad'.format(password))
print("Connected to server!")


def addConver(extension_json):
    query = "INSERT INTO {} VALUES {}"
    with engine.connect() as con:

        with open(extension_json) as f:
            chats_json = json.load(f)

        users = list(set([(chats_json[i]['idUser'],chats_json[i]['userName']) for i in range(len(chats_json))]))

        chats = list(set([(chats_json[i]['idChat']) for i in range(len(chats_json))]))

        for user in users:
            q = query.format('users (userName)',"('{}')".format(user[1]),'users.idUser')
            print(q)
            try:
                con.execute(q)
                #Get Response
                id = con.fetchone()[0]
                print(f"value inserted: {id}")
            except:
                print("At least I tried")
        
        for chat in chats:
            q = query.format('chats(idChat)',"({})".format(chat),'chats.idChat')
            print(q)
            try:
                con.execute(q)
                #Get Response
                id = con.fetchone()[0]
                print(f"value inserted: {id}")
            except:
                print("At least I tried")

        for message in chats_json:
            q = query.format('messages(text, datetime, users_idUser, chats_idChat)','("{}","{}",{},{})'.format(message['text'],message['datetime'],message['idUser'],message['idChat'],),'messages.idMessage')
            print(q)
            try:
                con.execute(q)
                #Get Response
                id = con.fetchone()[0]
                print(f"value inserted: {id}")
            except:
                print("At least I tried")

        return print('Done!')


def query(idUser):
    query = """
        SELECT * FROM users WHERE idUser='{}'
    """.format(idUser)
    print("Running query")
    print(query)
    df = pd.read_sql_query(query, engine)
    new = df.to_json(orient='records')
    return json.dumps(new)


@post('/add')
def add():
    print(dict(request.forms))
    autor=request.forms.get("autor")
    chiste=request.forms.get("chiste")  
    return {
        "inserted_doc": str(coll.addChiste(autor,chiste))}

@post('/user/create')
def addConver():
    query = "INSERT INTO conversation.users VALUES {}".format()
    with engine.connect() as con:
        for user in users:
            q = query.format('users (idUser, userName)',"({}, '{}')".format(user[0],user[1]),'users.idUser')
            print(q)
            try:
                con.execute(q)
                #Get Response
                id = con.fetchone()[0]
                print(f"value inserted: {id}")
            except:
                print("At least I tried")