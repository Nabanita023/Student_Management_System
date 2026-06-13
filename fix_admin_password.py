from werkzeug.security import generate_password_hash
import mysql.connector
from config import Config

# Create connection
conn = mysql.connector.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DATABASE
)
cursor = conn.cursor()

# Update admin password with proper hash
password_hash = generate_password_hash('admin123')
cursor.execute(
    "UPDATE users SET password_hash = %s WHERE username = %s",
    (password_hash, 'admin')
)
conn.commit()

print(f"✅ Admin password updated! Affected rows: {cursor.rowcount}")

cursor.close()
conn.close()
print("📝 Username: admin")
print("🔑 Password: admin123")