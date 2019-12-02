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
import function_api as fa
load_dotenv()

url = os.getenv("CONNECTION")
engine = db.create_engine(url)
print("Connected to server!")

# Select all users and idUser
@get('/Users/')
def totUsers():
    messages = fa.queryUsers()
    return json.dumps(messages)

# Select messages from idUser
@get('/Users/<idUser>')
def messUsers(idUser=0):
    messages = fa.queryUsermess(idUser)
    return json.dumps(messages)

'''
Create a user introducing name in URL.
If you wanna insert a full name you have to write %20 between first name and last name.

@post('/user/create/<name>')
def createUser(name):
    return json.dumps(fa.queryCreateUs(name))
'''

# Create a User in Database
@post('/user/create')
def createUser():
    name = str(request.forms.get('name'))
    return json.dumps(fa.queryCreateUs(name))

# Create a Chat in Database
@post('/chat/create')
def createChat():
    return fa.queryCreateChat()

# Create a Message in Database
@post('/chat/<chat_id>/addmessage')
def createMessage(chat_id):
    text = str(request.forms.get('text'))
    user = int(request.forms.get('user_id'))
    chat = chat_id
    return json.dumps(fa.queryCreateMess(text, user, chat))

# Select text from a chat
@get('/chat/<chat_id>/list')
def listMessages(chat_id):
    respond = fa.queryChat(chat_id)
    return json.dumps(respond)

#Sentiment analysis from messages in chats
@get('/chat/<chat_id>/sentiment')
def analyseChats(chat_id):
    respond = json.loads(fa.queryChat(chat_id))
    return json.dumps(fa.listSents(respond))

#Sentiment analysis from messages in users
@get('/users/<user_id>/sentiment')
def analyseUsers(user_id):
    respond = json.loads(fa.queryUsermess(user_id))
    return json.dumps(fa.listSents(respond))

#Select messages and UserName
@get('/message/<idUser>')
def messandUsers(idUser=0):
    respond = json.loads(fa.queryUserandMess(idUser))
    return json.dumps(respond)
    
run(host='localhost', port=8080)