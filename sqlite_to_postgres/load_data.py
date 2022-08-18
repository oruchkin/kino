from dataclasses import dataclass, fields, asdict
import sqlite3
from contextlib import contextmanager  
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import RealDictCursor
#from mover import open_slite_db
from dataclass import Film_work, Genre, Genre_Film_Work, Person, Person_Film_Work


def check_qutations(needed_data:str):
    """ этот скрипт заменяет одну кавыку ' на две '' иначе не вставиться в postgress """
    char_to_replace = {"'": "''"}
    result = ''
    for elem in needed_data:
        if elem in char_to_replace:
            result += char_to_replace[elem]
        else:
            result += elem
    return result
    

def get_values(data_obj: dataclass, columns:str):
    """Получение values необходимом формате"""
    columns = columns.split(',')
    values = ""
    counter = 0
    data_obj = asdict(data_obj)
    for i in range(len(columns)):
        field = columns[counter]
        counter +=1
        needed_data = str(data_obj[field])
        if needed_data == "None":
            needed_data = "NULL"
        else:
            needed_data = f"'{check_qutations(str(data_obj[field]))}'"
        values += needed_data
        if counter < len(columns):
            values += ", "
    values = "(" + values + ")"
    return values 
        
        
def save_data_to_postgres(pg_conn: psycopg2.extensions.connection, data_obj: dataclass, 
                          table_name: str, columns: str):
    """ загрузка данных в PostgreSQL """
    pg_cursor = pg_conn.cursor()
    insert_part = f'INSERT INTO content.{table_name}'
    values = get_values(data_obj,columns)
    query = (insert_part + ' (' + columns + ') VALUES ' + values + ' ON CONFLICT (id) DO NOTHING;')
    pg_cursor.execute(query)



def load_from_sqlite(sqlite_cursor: sqlite3.Connection, pg_conn: _connection):
    """ выгрузка данных из SQLite """
    
    """ Film_work Table """
    sqlite_cursor.execute("SELECT * FROM film_work;")
    data = sqlite_cursor.fetchall()
    all_film_work_data = []
    for i in data:
        all_film_work_data.append(Film_work(id = i["id"], 
                            title = i['title'],
                            description = i['description'],
                            creation_date = i['creation_date'],
                            file_path = i["file_path"],
                            rating = i['rating'],
                            type = i['type'],
                            created_at = i['created_at'],
                            updated_at = i['updated_at']))
    
    columns = tuple([field.name for field in fields(all_film_work_data[0])])
    columns = ','.join(columns)
    for data_obj in all_film_work_data:
        save_data_to_postgres(pg_conn, data_obj, 'film_work', columns)


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

    columns = tuple([field.name for field in fields(all_genre_data[0])])
    columns = ','.join(columns)
    for data_obj in all_genre_data:
        save_data_to_postgres(pg_conn, data_obj, 'genre', columns)


    """ Genre_Film_Work Table """    
    sqlite_cursor.execute("SELECT * FROM genre_film_work;")
    data = sqlite_cursor.fetchall()
    all_genre_fimwork_data = []
    for i in data:
        all_genre_fimwork_data.append(Genre_Film_Work(id = i["id"], 
                                film_work_id = i['film_work_id'],
                                genre_id = i['genre_id'],
                                created_at = i['created_at']))

    columns = tuple([field.name for field in fields(all_genre_fimwork_data[0])])
    columns = ','.join(columns)
    for data_obj in all_genre_fimwork_data:
        save_data_to_postgres(pg_conn, data_obj, 'genre_film_work', columns)


    """ Person Table """    
    sqlite_cursor.execute("SELECT * FROM person;")
    data = sqlite_cursor.fetchall()
    all_person_data = []
    for i in data:
        all_person_data.append(Person(id = i["id"], 
                    full_name = i['full_name'],
                    created_at = i['created_at'],
                    updated_at = i['updated_at']))

    columns = tuple([field.name for field in fields(all_person_data[0])])
    columns = ','.join(columns)
    for data_obj in all_person_data:
        save_data_to_postgres(pg_conn, data_obj, 'person', columns)


    """ Person_Film_Work Table """    
    sqlite_cursor.execute("SELECT * FROM person_film_work;")
    data = sqlite_cursor.fetchall()
    all_person_fimwork_data = []
    for i in data:
        all_person_fimwork_data.append(Person_Film_Work(id = i["id"], 
                                film_work_id = i['film_work_id'],
                                person_id = i['person_id'],
                                role = i['role'],
                                created_at = i['created_at']))

    columns = tuple([field.name for field in fields(all_person_fimwork_data[0])])
    columns = ','.join(columns)
    for data_obj in all_person_fimwork_data:
        save_data_to_postgres(pg_conn, data_obj, 'person_film_work', columns)


@contextmanager
def open_slite_db(db_path: str):
    """Подключение к базе sqlite"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn.cursor()
    conn.close()
    
    
def main():
    """Основная функция"""
    
    dsl = {'dbname': 'movies_db', 
           'user': 'app', 
           'password': '123qwe', 
           'host': '127.0.0.1', 
           'port': 5432}
    
    with open_slite_db('db.sqlite') as sqlite_cursor, \
        psycopg2.connect(**dsl, cursor_factory=RealDictCursor) as pg_conn:
        load_from_sqlite(sqlite_cursor, pg_conn)


if __name__ == '__main__':
    main()

