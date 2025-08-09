import mysql.connector
from mysql.connector import Error


class Databasecentralsystem:
    def __init__(self, host, user, password, database):
        self.db = sql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
def get_connection(self):
    try:
        return mysql.connector.connect(**self.db_config)
    except Error as e:
        return None

    
