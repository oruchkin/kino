import sqlite3
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from old.mover import open_slite_db
from dataclass import Film_work, Genre, Genre_Film_Work, Person, Person_Film_Work
from dataclasses import astuple, fields

def save_data_to_postgres(pg_conn: psycopg2.extensions.connection, data_list: list):
    print("ass")
    ass = pg_conn
    pg_cursor = pg_conn.cursor()
    #cols = [field.name for field in fields(data_list[0].__class__)]
    #print(cols)
    query = """INSERT INTO content.temp_table 
            (id, name, description, created_at , updated_at)
            VALUES
            ('3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 'Action', 'Nosne', '2021-06-16 20:14:09.309735+00', '2021-06-16 20:14:09.309765+00');
            """
    cols = [field for field in dict(data_list[0])]
    print(1)
    pg_cursor.execute(query)
    print(2)
    pg_cursor.commit()
    # pg_cursor.close()


def save_data_to_postgres(pg_conn: psycopg2.extensions.connection, data_list: list, table_name: str):
    print("ass")
    pg_cursor = pg_conn.cursor()
    insert_part = f'INSER INTO content.{table_name}'
    table_columns = (','.join([field for field in dict(data_list[0])]))
    query = insert_part + '(' + table_columns + ')' + 'VALUES' 
    #print(query)

    query = """INSERT INTO content.temp_table 
            (id, name, description, created_at , updated_at)
            VALUES
            ('3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 'Action', 'Nosne', '2021-06-16 20:14:09.309735+00', '2021-06-16 20:14:09.309765+00');
            """

    #pg_cursor.execute(query)

def load_from_sqlite(sqlite_cursor: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    
    # """ Film_work Table """
    # sqlite_cursor.execute("SELECT * FROM film_work;")
    # data = sqlite_cursor.fetchall()
    # all_film_work_data = []
    # for i in data:
    #     all_film_work_data.append(Film_work(id = i["id"], 
    #                         title = i['title'],
    #                         description = i['description'],
    #                         creation_date = i['creation_date'],
    #                         file_path = i["file_path"],
    #                         rating = i['rating'],
    #                         type = i['type'],
    #                         created_at = i['created_at'],
    #                         updated_at = i['updated_at']))
    

    """ Genre Table """    
    sqlite_cursor.execute("SELECT * FROM genre;")
    data = sqlite_cursor.fetchall()
    all_genre_data = []
    for i in data:
        all_genre_data.append(Genre(id = i["id"], 
                    name = i['name'],
                    description = i['description'],
                    created_at = i['created_at'],
                    updated_at = i['updated_at']))
    # print(all_genre_data[0])
    # print(type(all_genre_data[0]))
    save_data_to_postgres(pg_conn, data)

    # """ Genre_Film_Work Table """    
    # sqlite_cursor.execute("SELECT * FROM genre_film_work;")
    # data = sqlite_cursor.fetchall()
    # all_genre_fimwork_data = []
    # for i in data:
    #     all_genre_fimwork_data.append(Genre_Film_Work(id = i["id"], 
    #                             film_work_id = i['film_work_id'],
    #                             genre_id = i['genre_id'],
    #                             created_at = i['created_at']))


    # """ Person Table """    
    # sqlite_cursor.execute("SELECT * FROM person;")
    # data = sqlite_cursor.fetchall()
    # all_person_data = []
    # for i in data:
    #     all_person_data.append(Person(id = i["id"], 
    #                 full_name = i['full_name'],
    #                 created_at = i['created_at'],
    #                 updated_at = i['updated_at']))


    # """ Person_Film_Work Table """    
    # sqlite_cursor.execute("SELECT * FROM person_film_work;")
    # data = sqlite_cursor.fetchall()
    # all_person_fimwork_data = []
    # for i in data:
    #     all_person_fimwork_data.append(Person_Film_Work(id = i["id"], 
    #                             film_work_id = i['film_work_id'],
    #                             person_id = i['person_id'],
    #                             role = i['role'],
    #                             created_at = i['created_at']))

    
def main():
    """Основная функция"""
    
    dsl = {'dbname': 'movies_db', 
           'user': 'app', 
           'password': '123qwe', 
           'host': '127.0.0.1', 
           'port': 5432}
    
    with open_slite_db('db.sqlite') as sqlite_cursor, \
        psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        
        load_from_sqlite(sqlite_cursor, pg_conn)



if __name__ == '__main__':
    main()

