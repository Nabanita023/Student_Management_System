import mysql.connector
import os

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'localhost'),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', 'naba@123'),
        database=os.environ.get('MYSQL_DATABASE', 'student_management'),
        port=int(os.environ.get('MYSQL_PORT', 5000))
    )
    return conn