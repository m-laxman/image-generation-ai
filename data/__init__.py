import mysql
from mysql.connector import pooling
from dotenv import load_dotenv
import os
import threading

load_dotenv()


# Database Configuration
config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME'),
    'raise_on_warnings': True,
}


# Create a thread-local storage
local_storage = threading.local()

# Create a connection pool
# db_pool = pooling.MySQLConnectionPool(pool_name="pool", pool_size=10, **config)


class DatabaseContext:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()

    @property
    def cursor(self):
        return self._cursor

    # Exposing transactional methods for use in service layer
    def begin_transaction(self):
        self.connection.start_transaction()

    def commit_transaction(self):
        self.connection.commit()

    def rollback_transaction(self):
        self.connection.rollback()

    @cursor.setter
    def cursor(self, value):
        self._cursor = value


# Provide a global function to fetch the current context
def set_db_context():
    local_storage.db_context = DatabaseContext()

def get_current_db_context():
    local_storage.db_context = DatabaseContext()
    return getattr(local_storage, "db_context", None)
