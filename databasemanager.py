import psycopg2

class DatabaseManager:
    def __init__(self, database_url):
        self.database_url = database_url
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(self.database_url)
            self.connection.autocommit = True
            return self.connection
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
        
    def execute(self, query, params=None):
        try:
            if not self.connection:
                self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return cursor
        except Exception as e:
            print(f'Error executing query: {e}')
            return None
        
class DatabaseUrlManager:
    def __init__(self, username, password, host, database,port=5432):
        invalue_connection_params = False
        if not username:
            print("Can't have an empty username for database connection")
            invalue_connection_params = True
        if not password:
            print("Can't have blank password")
            invalue_connection_params = True
        if not host:
            print("Can't have no host")
            invalue_connection_params = True
        if not database:
            print("Can't have no database")
            invalue_connection_params = True
        
        if invalue_connection_params == True:
            self.url = None
        else:
            self.url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    def get_url(self):
        return self.url
        