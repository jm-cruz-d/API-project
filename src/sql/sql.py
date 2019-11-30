import sqlalchemy as db
import getpass

password = getpass.getpass("Insert your mysql root password: ")
engine = db.create_engine('mysql+pymysql://root:{}@localhost/conversation'.format(password))
print("Connected to server!")