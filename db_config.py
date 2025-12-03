import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",          # change
        password="anshu25", # change
        database="three_level_auth_db"
    )
    return conn
