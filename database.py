import mysql.connector


def get_db_connection():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='crowd_funding',
        auth_plugin='caching_sha2_password',
    )
    return db
