import unittest
import sqlite3
from xmlrpc.client import Boolean
import psycopg2
from psycopg2.extras import DictCursor
from dateutil.parser import parse


def connect_to_sqlite() -> sqlite3.Connection:
    """Подключение к базе sqlite"""
    db_path = '../db.sqlite'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn.cursor()


def connect_to_postgresql() -> psycopg2.extensions.connection:
    """Подключение к базе PostgreSql"""
    dsl = {'dbname': 'movies_db', 
        'user': 'app', 
        'password': '123qwe', 
        'host': '127.0.0.1', 
        'port': 5432}
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        return pg_conn
    
def count_raw_in_table(table_name:str, sqlite_cursor:sqlite3.Connection,
                       pg_cursor: psycopg2.extensions.cursor) -> dict:
    """ Считаем сколько рядов в таблице"""
    query = f"SELECT COUNT(*) FROM {table_name}"
    sqlite_cursor.execute(query)
    sqlite_count = int(sqlite_cursor.fetchone()[0])
    pg_cursor.execute(query)
    pg_count = int(dict(pg_cursor.fetchone())['count'])
    return {'sqlite_count' : sqlite_count, 'pg_count' : pg_count}


def get_columns_list_from_table(data: dict, db_name: str) -> dict:
    sqlite_columns = []
    postgres_columns = []
    if db_name == "sqlite":
        for i in data:
            sqlite_columns.append(i)
    elif db_name == "postgresql":
        for i in data:
            postgres_columns.append(i)
    return {"sqlite_columns":sqlite_columns, "postgres_columns":postgres_columns}


def compare_columns_in_table(postgres_columns:list, sqlite_columns:list) -> Boolean:
    """ Проверяем совпадают ли поля в таблице. """
    postgres_columns.sort()
    sqlite_columns.sort()
    return (postgres_columns == sqlite_columns)


def sort_dict(incoming_dict,columns) -> dict:
    """ Сортируем словарь для сравнения. """
    sorted_dict = {}
    for i in columns:
        try:
            # привод к одному формату времени если это поле времени
            sorted_dict[i] = parse(str(incoming_dict[i]))
        except:
            sorted_dict[i] = incoming_dict[i]
    return sorted_dict


def compare_data_in_table(sqlite_data,pg_data, columns) -> Boolean:
    """ Проверка содержимого таблиц разных баз данных. """
    counter = 0
    state = False
    for pg in pg_data:
        sqlite_sorted = sort_dict(sqlite_data[counter], columns)
        pg_sorted = sort_dict(pg, columns)
        state = (sqlite_sorted == pg_sorted)
        if state == False:
            return False
        counter += 1
    return True


class Test_adding(unittest.TestCase):
    def setUp(self):
        """ Устанавливаем соеденение с базами данных, получаем курсор. """
        self.sqlite_cursor = connect_to_sqlite()
        self.pg_cursor = connect_to_postgresql().cursor()
        
    def tearDown(self):
        self.sqlite_cursor.close()
        self.pg_cursor.close()
        
    def table_data(self, table):
        """ Функция для основной проверки всех таблиц. """
        # достаем данные sqlite
        self.sqlite_cursor.execute(f"SELECT * FROM {table} ORDER BY id;")
        sqlite_data = self.sqlite_cursor.fetchall()
        sqlite_columns = get_columns_list_from_table(dict(sqlite_data[0]), "sqlite")["sqlite_columns"]
        # достаем данные postgresql
        self.pg_cursor.execute(f"SELECT * FROM {table} ORDER BY id;")
        pg_data = self.pg_cursor.fetchall()
        postgres_columns = get_columns_list_from_table((dict(pg_data[0])), "postgresql")["postgres_columns"]
        # проверка колонок (fields)
        self.assertEqual(compare_columns_in_table(postgres_columns,sqlite_columns), True)
        # проверка реального содержимого таблиц (рядов)
        compare_result = compare_data_in_table(sqlite_data,pg_data, sqlite_columns)
        self.assertEqual(compare_result, True)
        
        
    def test_film_work_count(self):
        """ Проверяем кол-во на одинаковое кол-во фильмов в table film_work. """
        data = count_raw_in_table('film_work', self.sqlite_cursor, self.pg_cursor)
        self.assertEqual(data['sqlite_count'], data['pg_count'])
        
    def test_genre_count(self):
        """ Проверяем кол-во на одинаковое кол-во фильмов в table genre. """
        data = count_raw_in_table('genre', self.sqlite_cursor, self.pg_cursor)
        self.assertEqual(data['sqlite_count'], data['pg_count'])
        
    def test_genre_film_workcount(self):
        """ Проверяем кол-во на одинаковое кол-во фильмов в table genre_film_work. """
        data = count_raw_in_table('genre_film_work', self.sqlite_cursor, self.pg_cursor)
        self.assertEqual(data['sqlite_count'], data['pg_count'])
        
    def test_person_count(self):
        """ Проверяем кол-во на одинаковое кол-во фильмов в table person. """
        data = count_raw_in_table('person', self.sqlite_cursor, self.pg_cursor)
        self.assertEqual(data['sqlite_count'], data['pg_count'])
        
    def test_person_film_workcount(self):
        """ Проверяем кол-во на одинаковое кол-во фильмов в table person_film_work. """
        data = count_raw_in_table('person_film_work', self.sqlite_cursor, self.pg_cursor)
        self.assertEqual(data['sqlite_count'], data['pg_count'])
        
        
    def test_table_filmwork(self):
        """ Проверка целостности данных таблицы film_work. """
        table = "film_work"
        self.table_data(table)
        
    def test_table_genre(self):
        """ Проверка целостности данных таблицы genre. """
        table = "genre"
        self.table_data(table)
        
    def test_table_genre_film_work(self):
        """ Проверка целостности данных таблицы genre_film_work. """
        table = "genre_film_work"
        self.table_data(table)
        
    def test_table_person(self):
        """ Проверка целостности данных таблицы person. """
        table = "person"
        self.table_data(table)
        
    def test_table_person_film_work(self):
        """ Проверка целостности данных таблицы person_film_work. """
        table = "person_film_work"
        self.table_data(table)
            
        
def main():
    unittest.main()
        
if __name__ == '__main__':
    main()
