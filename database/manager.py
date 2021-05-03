# made by https://github.com/jubnl


import pymysql.cursors
from pymysql.connections import Connection
from pymysql.cursors import DictCursor
from database import *


class Database():

    def __init__(self,
                 host: str = DB_HOST,
                 port: int = DB_PORT,
                 user: str = DB_USER,
                 password: str = DB_PASSWORD,
                 database: str = DB_NAME) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def connection(self) -> Connection:
        """
        Database connection : return a pymysql.connections.Connexion object
        """

        # Create a pymysql.connexions.Connexion object and return it
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset = "utf8mb4",
            cursorclass=DictCursor
        )
