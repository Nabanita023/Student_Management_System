from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from db import get_db_connection
from routes.auth import login_required

students_bp = Blueprint('students_bp', __name__)

@students_bp.route('/')
@login_required
def list_students():
    print(">>> MAIN ROUTE HIT! <<<")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    
    print(f"Found {len(students)} students")
    return render_template('students/list.html', students=students)

@students_bp.route('/debug-data')
@login_required
def debug_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'count': len(students), 'students': students})

@students_bp.route('/view/<int:id>')
@login_required
def view_student(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()
    cursor.execute("""
        SELECT c.*, e.grade, e.status, e.enroll_date 
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        WHERE e.student_id = %s
    """, (id,))
    enrolled_courses = cursor.fetchall()
    cursor.close()
    conn.close()
    
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('students_bp.list_students'))
    return render_template('students/view.html', student=student, enrolled_courses=enrolled_courses)

@students_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form.get('address', '')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, email, phone, address) VALUES (%s, %s, %s, %s)",
            (name, email, phone, address)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Student added successfully!', 'success')
        return redirect(url_for('students_bp.list_students'))
    
    return render_template('students/add.html')

@students_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form.get('address', '')
        cursor.execute(
            "UPDATE students SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s",
            (name, email, phone, address, id)
        )
        conn.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('students_bp.list_students'))
    
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('students/edit.html', student=student)

@students_bp.route('/delete/<int:id>')
@login_required
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM enrollments WHERE student_id = %s", (id,))
    enrollment_count = cursor.fetchone()[0]
    
    if enrollment_count > 0:
        flash(f'Cannot delete student with {enrollment_count} enrollment(s).', 'danger')
    else:
        cursor.execute("DELETE FROM students WHERE id = %s", (id,))
        conn.commit()
        flash('Student deleted successfully!', 'success')
    
    cursor.close()
    conn.close()
    return redirect(url_for('students_bp.list_students'))