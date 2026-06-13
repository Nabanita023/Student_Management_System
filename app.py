from flask import Flask, render_template, redirect, url_for, request, flash, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from config import Config
from db import get_db_connection

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Import blueprints
from routes.home import home_bp
from routes.students import students_bp
from routes.courses import courses_bp
from routes.enrollments import enrollments

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(students_bp, url_prefix='/students')
app.register_blueprint(courses_bp, url_prefix='/courses')
app.register_blueprint(enrollments, url_prefix='/enrollments')

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password', 'danger')
            return redirect(url_for('login'))
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                # Verify password
                if check_password_hash(user['password_hash'], password):
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    flash('Login successful!', 'success')
                    return redirect(url_for('home_bp.home'))
                else:
                    flash('Invalid password', 'danger')
            else:
                flash('Username not found. Please register first.', 'danger')
        else:
            flash('Database connection error. Please try again.', 'danger')
        
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/join-us', methods=['GET', 'POST'])
def join_us():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if not username or not password:
            flash('Username and password are required', 'danger')
            return redirect(url_for('join_us'))
        
        # Hash the password
        password_hash = generate_password_hash(password)
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
                    (username, password_hash, email)
                )
                conn.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except mysql.connector.IntegrityError:
                flash('Username already exists. Please choose another.', 'danger')
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Database connection error', 'danger')
    
    return render_template('join_us.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# About route
@app.route('/about')
def about():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# Home route
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home_bp.home'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)