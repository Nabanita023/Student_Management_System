import mysql.connector
from config import Config

conn = mysql.connector.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DATABASE
)
cursor = conn.cursor()

print("=== Enrollments Table Structure ===")
cursor.execute("DESCRIBE enrollments")
for col in cursor.fetchall():
    print(f"  • {col[0]} ({col[1]})")

print("\n=== Sample Data ===")
cursor.execute("SELECT * FROM enrollments LIMIT 3")
for row in cursor.fetchall():
    print(f"  {row}")

cursor.close()
conn.close()