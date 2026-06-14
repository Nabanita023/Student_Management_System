from werkzeug.security import generate_password_hash
import mysql.connector
from config import Config

def create_admin():
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        existing_admin = cursor.fetchone()
        if existing_admin:
            print("⚠️ Admin user already exists!")
        else:
            password_hash = generate_password_hash('admin')
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
                ('admin', password_hash, 'admin@example.com')
            )
            conn.commit()
            print("✅ Admin created! Username: admin | Password: admin")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")

if __name__ == "__main__":
    create_admin()