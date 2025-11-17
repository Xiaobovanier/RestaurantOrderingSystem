
import pymysql
from pymysql.cursors import DictCursor
from db_config import HOST, USER, PASSWORD, DB, CHARSET

def get_conn():
    return pymysql.connect(
        host=HOST, user=USER, passwd=PASSWORD, db=DB, charset=CHARSET,
        cursorclass=DictCursor, autocommit=False
    )

def query(sql, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()
    finally:
        conn.close()

def execute(sql, params=None, many=False):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            if many:
                cur.executemany(sql, params or [])
            else:
                cur.execute(sql, params or ())
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def execute_returning_id(sql, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            last_id = cur.lastrowid
        conn.commit()
        return last_id
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
