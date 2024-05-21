import threading
import sqlite3
from queue import Queue
from typing import Optional

class DBConnectionPool:
    __instance = None
    __lock = threading.Lock()

    def __new__(cls):
        with cls.__lock:
            if not cls.__instance:
                cls.__instance = super().__new__(cls)
                cls.__instance._initialize_pool()
        return cls.__instance

    def __init__(self):
        self.__connections: Optional[Queue] = None
        self.__max_connections: Optional[int] = None

    def _initialize_pool(self):
        self.__max_connections = 10
        self.__connections = Queue(maxsize=self.__max_connections)
        for _ in range(self.__max_connections):
            self.__connections.put(self._create_connection())

    @staticmethod
    def _create_connection():
        db_connection = "database.db"
        connection = sqlite3.connect(db_connection)
        return connection

    @staticmethod
    def _create_database():
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS example (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO example (name) VALUES ('Amr')")
        cursor.execute("INSERT INTO example (name) VALUES ('Ahmed')")
        cursor.execute("INSERT INTO example (name) VALUES ('Hossam')")
        connection.commit()
        connection.close()

    def get_connection(self):
        if self.__connections is None:
            self._initialize_pool()
        if self.__connections.empty():
            raise RuntimeError("Maximum number of connections reached")
        return self.__connections.get()

    def release_connection(self, connection):
        self.__connections.put(connection)

    def close_all_connections(self):
        while not self.__connections.empty():
            connection = self.__connections.get()
            connection.close()
