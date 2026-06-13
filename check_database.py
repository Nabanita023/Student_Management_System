from db import get_db_connection

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)

print("=" * 50)
print("DATABASE CHECK")
print("=" * 50)

# Check students table
cursor.execute("SELECT COUNT(*) as count FROM students")
count = cursor.fetchone()
print(f"Total students in database: {count['count']}")

# Get all students
cursor.execute("SELECT id, name, email, phone FROM students")
students = cursor.fetchall()

if students:
    print("\nStudents found:")
    for student in students:
        print(f"  ID: {student['id']}, Name: {student['name']}, Email: {student['email']}")
else:
    print("\nNo students found in database!")

cursor.close()
conn.close()