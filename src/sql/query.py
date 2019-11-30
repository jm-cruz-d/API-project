import sqlalchemy as db
import getpass
import pandas as pd

password = getpass.getpass("Insert your mysql root password: ")
engine = db.create_engine('mysql+pymysql://root:{}@localhost/conversation'.format(password))
print("Connected to server!")

def query(idUser=0):
    query = """
        SELECT * FROM messages WHERE idUser='{}'
    """.format(idUser)
    print("Running query")
    print(query)
    df = pd.read_sql_query(query, engine)
    return df