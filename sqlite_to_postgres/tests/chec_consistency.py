import unittest
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor


def open_slite_db():
    """Подключение к базе sqlite"""
    db_path = '../db.sqlite'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn.cursor()


def connect_to_postgresql():
    """Подключение к базе PostgreSql"""
    dsl = {'dbname': 'movies_db', 
        'user': 'app', 
        'password': '123qwe', 
        'host': '127.0.0.1', 
        'port': 5432}
    with psycopg2.connect(**dsl, cursor_factory=RealDictCursor) as pg_conn:
        return pg_conn
    
    
def count_raw_in_db(table_name, sqlite_cursor, pg_cursor):
    query = f"SELECT COUNT(*) FROM {table_name}"
    sqlite_cursor.execute(query)
    sqlite_count = int(sqlite_cursor.fetchone()[0])
    pg_cursor.execute(query)
    pg_count = int(dict(pg_cursor.fetchone())['count'])
    result = {'sqlite_count' : sqlite_count, 'pg_count' : pg_count}
    return result


class Test_adding(unittest.TestCase):
    def setUp(self):
        self.sqlite_cursor = open_slite_db()
        self.pg_cursor = connect_to_postgresql().cursor()
        

    def test_film_work_count(self):
        """ Проверяем кол-во на одинаковое кол-во фильмов в table film_work """
        data = count_raw_in_db('film_work', self.sqlite_cursor, self.pg_cursor)
        print(data)
        self.assertEqual(data['sqlite_count'], data['pg_count'])
        
        
    def test_genre_count(self):
        """ Проверяем кол-во на одинаковое кол-во фильмов в table genre """
        data = count_raw_in_db('genre', self.sqlite_cursor, self.pg_cursor)
        print(data)
        self.assertEqual(data['sqlite_count'], data['pg_count'])
        

    def test_genre_film_workcount(self):
        """ Проверяем кол-во на одинаковое кол-во фильмов в table genre_film_work """
        data = count_raw_in_db('genre_film_work', self.sqlite_cursor, self.pg_cursor)
        print(data)
        self.assertEqual(data['sqlite_count'], data['pg_count'])
        
        
    def test_person_count(self):
        """ Проверяем кол-во на одинаковое кол-во фильмов в table person """
        data = count_raw_in_db('person', self.sqlite_cursor, self.pg_cursor)
        print(data)
        self.assertEqual(data['sqlite_count'], data['pg_count'])
        
        
    def test_person_film_workcount(self):
        """ Проверяем кол-во на одинаковое кол-во фильмов в table person_film_work """
        data = count_raw_in_db('person_film_work', self.sqlite_cursor, self.pg_cursor)
        print(data)
        self.assertEqual(data['sqlite_count'], data['pg_count'])

        
if __name__ == '__main__':
    unittest.main()