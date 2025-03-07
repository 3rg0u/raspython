import mysql.connector as mysql

DB_CONFIG = {
    "host": "localhost",
    "user": "username",
    "password": "pw",
    "database": "db_name",
}


def fetch_pass():
    global DB_CONFIG
    _db = mysql.connect(**DB_CONFIG)
    _cursor = _db.cursor()
    _SQL = '''select pass from passwords where user="nqaisme"'''
    _cursor.execute(_SQL)
    return _cursor.fetchone()[0]
