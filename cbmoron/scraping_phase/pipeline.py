import psycopg2


class PostgreSQLConnection:
    def __init__(self, host, database, username, password):
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.conn = None
        self.cursor = None
 
    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.username,
            password=self.password
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def execute(self, query, params=None):
        self.cursor.execute("BEGIN")
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            with open('querying.txt','a') as file:
                file.write(f'{type(e)},{e}\n')
            self.conn.rollback()

    def fetchall(self):
        return self.cursor.fetchall()
    


class DataPipeline:
    def __init__(self, conn, table_name=''):
        self.conn = conn
        self.table_name = table_name

    def insert_data(self, dataframe):
        try:
            columns = dataframe.columns.tolist()
            placeholders = ', '.join(['%s' for _ in columns])
            insert_query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"

            for index, row in dataframe.iterrows():
                self.conn.execute(insert_query, list(row))
        except Exception as e:
            print(e,type(e))
            print('Error en insert data')
    
    def query(self,query):
        try:
            self.conn.execute(query)
            return self.conn.fetchall()
        except Exception as e:
            print(f'Error query {e}')
