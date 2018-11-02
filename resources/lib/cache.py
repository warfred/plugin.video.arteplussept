import sqlite3
import json
import zlib


_cache_name = ''
_cache_db = ''
_cache_db_cursor = ''


def open_cache_db(db_name):
    mydb = sqlite3.connect(db_name)
    return mydb


def open_cache_db_conn(db):
    conn = db.cursor()
    return conn


def check_cache_table(db_curs, db_table):
    sql = 'PRAGMA table_info('+ db_table + ')'

    try:
        if db_curs.execute( sql ).fetchone() is not None:
           # something wrong hapend
           return False
    except sqlite3.Error as e:
        return False

    return True


def create_cache_db(db, db_conn, create):
    db_conn.execute(create)
    db.commit()


def is_cache_db_entry( db_conn, db_curs, db_table, date ):
    with db_conn:
        sql_check = 'SELECT count(*) FROM ' + db_table + ' WHERE date="'+date+'"'
        if db_curs.execute( sql_check ).fetchone()[0] != 0:
            return True

        return False

    return None


def store_cache_db(db_conn, db_curs, db_table, date, dict):
    with db_conn:
        if not is_cache_db_entry(db_conn, db_curs, db_table, date):
            sql = 'INSERT INTO ' + db_table + ' values (?, ?)'
            try:
                db_curs.execute( sql , ( date, sqlite3.Binary(zlib.compress(json.dumps(dict),5) )) )
                db_conn.commit
            except sqlite3.Error as e:
                return False

            return True
        else:
            return False

    return False


def get_cache_db(db_conn, db_curs, db_table, date ):
    with db_conn:
        if is_cache_db_entry(db_conn, db_curs, db_table, date):
            sql = 'SELECT dict FROM ' + db_table + ' WHERE date="'+date+'"'
            try:
		dict = json.loads(str(sqlite3.Binary(zlib.decompress(str(db_curs.execute( sql ).fetchone()[0])))))
	    except sqlite3.Error as e:
                return None

            return dict
        else:
            return None

    return None
        

def close_cache_db(db):
    db.close


def close_cache_db_conn(db_conn):
    db_conn.close

