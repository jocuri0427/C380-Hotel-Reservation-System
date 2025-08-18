import mysql.connector
from mysql.connector import Error


class Databasecentralsystem:
    def __init__(self, host='localhost', user='root', password='Chidera23', database='hotel'):
        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }

    def get_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except Error as e:
            print("database error", e)
            raise  # Re-raise the exception to be handled by the caller
