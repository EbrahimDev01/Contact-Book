import mysql.connector


class DatabaseContext:
    def __init__(self, got_database='', got_host='localhost', got_user='root', got_password=''):
        self.connection = mysql.connector.connect(
            host=got_host,
            user=got_user,
            passwd=got_password,
            database=got_database
        )
        self.cursor = self.connection.cursor()

    def execute_database(self, got_sql_command, got_value=(), got_multi=False):
        self.cursor.execute(got_sql_command, got_value, got_multi)

    def create_database(self, got_database_name):
        sql_command = 'CREATE DATABASE IF NOT EXISTS ' + got_database_name
        self.execute_database(sql_command)

    def close_database(self):
        self.connection.close()

    def commit_database(self):
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()
