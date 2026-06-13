import mysql.connector
from config import Config

conn = mysql.connector.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DATABASE
)
cursor = conn.cursor()

# First, check if students table exists and has data
cursor.execute("SELECT COUNT(*) FROM students")
count = cursor.fetchone()[0]

if count == 0:
    print("Adding sample students...")
    students = [
        ('John Doe', 'john@example.com', '1234567890', '123 Main St, New York'),
        ('Jane Smith', 'jane@example.com', '0987654321', '456 Oak Ave, Los Angeles'),
        ('Mike Johnson', 'mike@example.com', '5551234567', '789 Pine Rd, Chicago'),
        ('Sarah Williams', 'sarah@example.com', '5559876543', '321 Elm St, Houston'),
        ('David Brown', 'david@example.com', '5554567890', '654 Maple Dr, Phoenix'),
    ]
    
    cursor.executemany(
        "INSERT INTO students (name, email, phone, address) VALUES (%s, %s, %s, %s)",
        students
    )
    conn.commit()
    print(f"✅ Added {cursor.rowcount} students successfully!")
else:
    print(f"Students table already has {count} students")

# Show current students
cursor.execute("SELECT id, name, email FROM students")
print("\n📊 Current Students:")
for student in cursor.fetchall():
    print(f"  - ID: {student[0]}, Name: {student[1]}, Email: {student[2]}")

cursor.close()
conn.close()