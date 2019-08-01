import psycopg2


class DBHandler:
    def __init__(self, user, password, host, database, port=5432):
        self.connected = False
        try:
            self.connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
            self.cursor = self.connection.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            self.error_msg = error
            return

        self.connected = True

    def create_tables(self):
        create_table_query = '''CREATE TABLE IF NOT EXISTS Persons
              (ID INT PRIMARY KEY NOT NULL,
              Name            TEXT NOT NULL,
              Category        TEXT,
              URL             TEXT,
              Image_URL       TEXT,
              Timestamp       timestamp); '''

        self.execute(create_table_query)

    def clear_table(self, table_name):
        truncate_table_query = f'TRUNCATE TABLE {table_name}'

        self.execute(truncate_table_query)

    def add_person(self, pid, name, category, url, image_url, timestamp):
        insert_person_query = f"""INSERT INTO Persons (ID, Name, Category, URL, Image_URL, Timestamp)
                                VALUES ({pid}, '{name}', '{category}', '{url}', '{image_url}', '{timestamp}');"""

        #print(insert_person_query)
        self.execute(insert_person_query)
        print(f'{name} added to db, category: {category}')

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")