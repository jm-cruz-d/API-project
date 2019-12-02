import sqlalchemy as db
import os
import pandas as pd
import json
import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from bson.json_util import dumps
from sqlalchemy.sql import text
import sqlalchemy as db
from bottle import route, run, template, get, post, request
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("CONNECTION")
engine = db.create_engine(url)
print("Connected to server!")

# Add json's files in a SQL Database
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


def queryUsers():
    query = """
        SELECT * FROM users
    """
    print(f"Running query: {query}")
    df = pd.read_sql_query(query, engine)
    new = df.to_json(orient='records')
    return new

def queryUsermess(idUser):
    query = """
        SELECT text FROM messages WHERE users_idUser='{}'
    """.format(idUser)
    print(f"Running query: {query}")
    df = pd.read_sql_query(query, engine)
    new = df.to_json(orient='records')
    return new

def queryCreateUs(name):
    query = "INSERT INTO users (userName) VALUES ('{}')".format(name)
    with engine.connect() as con:
        con.execute(query)
    q = """
        SELECT * FROM users WHERE userName='{}'
    """.format(name)
    print(f"Running query: {q}")
    df = pd.read_sql_query(q, engine)
    new = df.to_json(orient='records')
    return new

def queryCreateChat():
    with engine.connect() as con:
        number_chat = list(con.execute("SELECT idChat FROM chats ORDER BY idChat DESC LIMIT 1"))
        new_chatId = number_chat[0][0]+1
    with engine.connect() as con:
        query = "INSERT INTO chats (idChat) VALUES ({})".format(new_chatId)
        con.execute(query)
    return {f'{new_chatId}': 'Created chat'}

def queryCreateMess(text, user, chat):
    query = '''INSERT INTO messages (text, datetime, users_idUser, chats_idChat) VALUES ('{}', CURRENT_TIMESTAMP, {}, {})'''.format(text, user, chat)
    with engine.connect() as con:
        con.execute(query)
    
    q = """
        SELECT idMessage FROM messages WHERE text='{}'
    """.format(text)
    print(f"Running query: {q}")
    df = pd.read_sql_query(q, engine)
    new = df.to_json(orient='records')
    return new

def queryChat(chat_id):
    query = """
        SELECT users_idUser, text FROM messages WHERE chats_idChat='{}'
    """.format(chat_id)
    print(f"Running query: {query}")
    df = pd.read_sql_query(query, engine)
    new = df.to_json(orient='records')
    return new

def mediaChat(list_name):
    x = round(sum([v['neg'] for dat in list_name for k, v in dat.items()])/len(list_name), 3)
    y = round(sum([v['neu'] for dat in list_name for k, v in dat.items()])/len(list_name), 3)
    z = round(sum([v['pos'] for dat in list_name for k, v in dat.items()])/len(list_name), 3)
    return x, y, z

def listSents(respond):
    sid = SentimentIntensityAnalyzer()
    lst = []
    for sent in respond:
        lst.append({sent['text'] : sid.polarity_scores(sent['text'])})
    x, y, z = mediaChat(lst)
    lst.insert(0, {'user media': {'neg': x, 'neu': y, 'pos': z}})
    return lst

def queryUserandMess(idUser):
    query = """
        SELECT users.userName, messages.text
	from messages join
	users
	on messages.users_idUser = users.idUser
	WHERE messages.users_idUser = {};
    """.format(idUser)
    print(f"Running query: {query}")
    df = pd.read_sql_query(query, engine)
    new = df.to_json(orient='records')
    return new