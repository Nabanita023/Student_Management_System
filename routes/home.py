from flask import Blueprint, render_template, session
from db import get_db_connection

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/')
def home():
    if 'user_id' not in session:
        return render_template('login.html')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM courses")
    total_courses = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM enrollments")
    total_enrollments = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return render_template('home.html', 
                         total_students=total_students,
                         total_courses=total_courses,
                         total_enrollments=total_enrollments)

# Add this route to home.py
@home_bp.route('/about')
def about():
    return render_template('home.html')  # About section is in home page