import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kylliann2110", 
            database="database_solana"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def verif_tables(self):
        try:
            self.execute("SHOW TABLES")
            tables = [table['Tables_in_gestion_financiere1'] for table in self.cursor]

            if not all(table in tables for table in ['users', 'accounts', 'categories', 'transactions']):
                with open('schema.sql', 'r') as f:
                    sql_script = f.read()
                for statement in sql_script.split(';'):
                    if statement.strip():
                        self.execute(statement)
                self.commit()
        except mysql.connector.Error as err:
            print(f"Database error : {err}")
Database.verif_tables