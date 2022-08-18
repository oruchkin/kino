
import logging
import sqlite3
from contextlib import contextmanager  


    
@contextmanager
def open_slite_db(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn.cursor()
    conn.commit()
    conn.close()
        
        

