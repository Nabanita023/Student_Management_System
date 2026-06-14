from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection
from routes.auth import login_required

enrollments = Blueprint('enrollments', __name__)

@enrollments.route('/')
@login_required
def list_enrollments():
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed!', 'danger')
        return render_template('enrollments/list.html', enrollments=[])
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.*, s.name as student_name, c.name as course_name 
        FROM enrollments e
        JOIN students s ON e.student_id = s.id
        JOIN courses c ON e.course_id = c.id
    """)
    enrollments_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('enrollments/list.html', enrollments=enrollments_list)


@enrollments.route('/enroll', methods=['GET', 'POST'])
@login_required
def enroll_student():
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed!', 'danger')
        return render_template('enrollments/enroll.html', students=[], courses=[])

    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'POST':
            student_id = request.form['student_id']
            course_id  = request.form['course_id']
            grade      = request.form.get('grade', 'Pending')
            cursor.execute(
                "INSERT INTO enrollments (student_id, course_id, grade) VALUES (%s, %s, %s)",
                (student_id, course_id, grade)
            )
            conn.commit()
            flash('Student enrolled successfully!', 'success')
            return redirect(url_for('enrollments.list_enrollments'))

        cursor.execute("SELECT id, name FROM students ORDER BY name")
        students = cursor.fetchall()
        cursor.execute("SELECT id, name as course_name FROM courses ORDER BY name")
        courses = cursor.fetchall()
        return render_template('enrollments/enroll.html', students=students, courses=courses)

    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('enrollments/enroll.html', students=[], courses=[])

    finally:
        cursor.close()
        conn.close()


@enrollments.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_enrollment(id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed!', 'danger')
        return redirect(url_for('enrollments.list_enrollments'))

    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'POST':
            student_id = request.form['student_id']
            course_id  = request.form['course_id']
            grade      = request.form.get('grade', 'Pending')
            cursor.execute(
                "UPDATE enrollments SET student_id=%s, course_id=%s, grade=%s WHERE id=%s",
                (student_id, course_id, grade, id)
            )
            conn.commit()
            flash('Enrollment updated successfully!', 'success')
            return redirect(url_for('enrollments.list_enrollments'))

        cursor.execute("""
            SELECT e.*, s.name as student_name, c.name as course_name
            FROM enrollments e
            JOIN students s ON e.student_id = s.id
            JOIN courses c ON e.course_id = c.id
            WHERE e.id = %s
        """, (id,))
        enrollment = cursor.fetchone()

        if not enrollment:
            flash('Enrollment not found!', 'danger')
            return redirect(url_for('enrollments.list_enrollments'))

        cursor.execute("SELECT id, name FROM students ORDER BY name")
        students = cursor.fetchall()
        cursor.execute("SELECT id, name as course_name FROM courses ORDER BY name")
        courses = cursor.fetchall()

        return render_template('enrollments/update_enrollment.html',
                               enrollment=enrollment,
                               students=students,
                               courses=courses)

    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('enrollments.list_enrollments'))

    finally:
        cursor.close()
        conn.close()


@enrollments.route('/update-grade/<int:id>', methods=['GET', 'POST'])
@login_required
def update_grade(id):
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed!', 'danger')
        return redirect(url_for('enrollments.list_enrollments'))

    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'POST':
            grade = request.form['grade']
            cursor.execute(
                "UPDATE enrollments SET grade=%s WHERE id=%s",
                (grade, id)
            )
            conn.commit()
            flash('Grade updated successfully!', 'success')
            return redirect(url_for('enrollments.list_enrollments'))

        cursor.execute("SELECT * FROM enrollments WHERE id = %s", (id,))
        enrollment = cursor.fetchone()

        if not enrollment:
            flash('Enrollment not found!', 'danger')
            return redirect(url_for('enrollments.list_enrollments'))

        return render_template('enrollments/update_grade.html', enrollment=enrollment)

    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('enrollments.list_enrollments'))

    finally:
        cursor.close()
        conn.close()