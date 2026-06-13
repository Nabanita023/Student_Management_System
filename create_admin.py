from werkzeug.security import generate_password_hash
import mysql.connector
from config import Config

def create_admin():
    try:
        # Create connection
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("✅ Users table created/verified")
        
        # Check if admin already exists
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        existing_admin = cursor.fetchone()
        
        if existing_admin:
            print("⚠️ Admin user already exists!")
            print("📝 Username: admin")
            print("🔑 If you forgot password, run password reset script")
        else:
            # Create admin user (password: admin123)
            password_hash = generate_password_hash('admin123')
            cursor.execute("""
            INSERT INTO users (username, password_hash, email) 
            VALUES (%s, %s, %s)
            """, ('admin', password_hash, 'admin@example.com'))
            conn.commit()
            print("✅ Admin user created successfully!")
            print("📝 Username: admin")
            print("🔑 Password: admin123")
            print("📧 Email: admin@example.com")
        
        # Show all users
        cursor.execute("SELECT id, username, email, created_at FROM users")
        users = cursor.fetchall()
        print(f"\n📊 Total users in database: {len(users)}")
        for user in users:
            print(f"   - ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔧 Setting up admin user...")
    create_admin()
    print("\n✨ Setup complete! You can now run: python app.py")