
#from .dataclass import Film_work, Genre, Genre_Film_Work, Person, Person_Film_Work
import psycopg2
from old.mover import open_slite_db

#def save_film_work_to_postgres(conn: psycopg2.extensions.connection, film_work: Film_work):
#    pass





# def load_from_sqlite(sqlite_cursor):
#     sqlite_cursor.execute("SELECT * FROM film_work;") 
#     data = sqlite_cursor.fetchall()
#     for i in data:
#         print(dict(i))
#     #return



    
    
def main():
    with open_slite_db('db.sqlite') as sqlite_cursor:
        print(123)
    
if __name__ == '__main__': 
    main()