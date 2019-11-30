import sqlalchemy as db
import getpass

password = getpass.getpass("Insert your mysql root password: ")
engine = db.create_engine('mysql+pymysql://root:{}@localhost/conversation'.format(password))
print("Connected to server!")


def addConver(extension_json):
    with open(f'{extension_json}') as f:
        chats_json = json.load(f)

    query = "INSERT INTO {} VALUES {} RETURNING {}"
    users = list(set([(chats_json[i]['idUser'],chats_json[i]['userName']) for i in range(len(chats_json))]))
    chats = list(set([(chats_json[i]['idChat']) for i in range(len(chats_json))]))
    
    for user in users:
    q = query.format('users (idUser, userName)',"({}, '{}')".format(user[0],user[1]),'users.idUser')
    print(q)
    try:
        cur.execute(q)
        #Get Response
        id = cur.fetchone()[0]
        print(f"value inserted: {id}")
    except:
        print("At least I tried")

    for chat in chats:
    q = query.format('chats(idChat)',"({})".format(chat),'chats.idChat')
    print(q)
    try:
        cur.execute(q)
        #Get Response
        id = cur.fetchone()[0]
        print(f"value inserted: {id}")
    except:
        print("At least I tried")

    for message in chats_json:
    q = query.format('messages(idMessage, text, datetime, users_idUser, chats_idChat)',"({},'{}','{}',{},{})".format(message['idMessage'],message['text'],message['datetime'],message['idUser'],message['idChat'],),'messages.idMessage')
    print(q)
    try:
        cur.execute(q)
        #Get Response
        id = cur.fetchone()[0]
        print(f"value inserted: {id}")
    except:
        print("At least I tried")
        
    print('Done!')

