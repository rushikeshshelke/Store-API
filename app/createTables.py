import sqlite3
from globalVariables import GlobalVariables

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

cursor.execute(GlobalVariables.CREATE_USERS_TABLE)
cursor.execute(GlobalVariables.CREATE_ITEMS_TABLE)

connection.commit()

connection.close()