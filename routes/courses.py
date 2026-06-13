from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection
from routes.auth import login_required

courses_bp = Blueprint('courses_bp', __name__)

@courses_bp.route('/')
@login_required
def list_courses():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('courses/list.html', courses=courses)

@courses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_course():
    if request.method == 'POST':
        # Match your database columns
        name = request.form['name']
        description = request.form['description']
        duration = request.form['duration']
        fees = request.form['fees']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO courses (name, description, duration, fees) VALUES (%s, %s, %s, %s)",
            (name, description, duration, fees)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Course added successfully!', 'success')
        return redirect(url_for('courses_bp.list_courses'))
    
    return render_template('courses/add.html')

@courses_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_course(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        duration = request.form['duration']
        fees = request.form['fees']
        
        cursor.execute(
            "UPDATE courses SET name=%s, description=%s, duration=%s, fees=%s WHERE id=%s",
            (name, description, duration, fees, id)
        )
        conn.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('courses_bp.list_courses'))
    
    cursor.execute("SELECT * FROM courses WHERE id = %s", (id,))
    course = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('courses/edit.html', course=course)

@courses_bp.route('/delete/<int:id>')
@login_required
def delete_course(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('courses_bp.list_courses'))