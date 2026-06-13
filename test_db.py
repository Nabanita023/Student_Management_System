from db import get_db_connection, test_connection

# Test the connection
if test_connection():
    print("✓ Database is ready!")
    
    # Try to get actual connection
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✓ MySQL Version: {version[0]}")
        cursor.close()
        conn.close()
else:
    print("✗ Database connection failed. Check your config.py settings")