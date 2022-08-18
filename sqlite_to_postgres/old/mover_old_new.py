
import logging
import sqlite3
from contextlib import contextmanager  

@contextmanager
def conn_context(db_path: str):
    print(1)
    conn = sqlite3.connect(db_path) # Устанавливаем соединение с БД
    conn.row_factory = sqlite3.Row # По-умолчанию SQLite возвращает строки в виде кортежа значений. Эта строка указывает, что данные должны быть в формате «ключ-значение»
    yield conn # С конструкцией yield вы познакомитесь в следующем модуле 
    # Пока воспринимайте её как return, после которого код может продолжить выполняться дальше
    print(4)
    conn.close() 
    


db_path = 'db.sqlite'
print(0)
with conn_context(db_path) as conn:
    print(2)
    curs = conn.cursor() # Получаем курсор (a result set (a set of data rows) and perform complex logic on a row by row basis)
    curs.execute("SELECT * FROM film_work;") # Формируем запрос. Внутри execute находится обычный SQL-запрос
    data = curs.fetchall() # Получаем данные
    counter = 0
    # for i in data:
    #     counter +=1
    #     print(dict(i))
    print(counter)
    print(3)
    
    
    
    
db_path = 'db.sqlite'
try:
    print("hohoho")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()
    curs.execute("SELECT * FROM film_work;") 
    data = curs.fetchall()
    # for i in data:
    #     print(dict(i))
finally:
    logging.info("Closing conection")
    conn.close()
    
    
    
print("zad")
@contextmanager
def open_slite_db(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn.cursor()
    conn.commit() #сохранить изменения
    conn.close()
        
        
