CREATE DATABASE IF NOT EXISTS student_management;
USE student_management;

-- Table  1: student

CREATE TABLE IF NOT EXISTS students (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(100) UNIQUE NOT NULL,
    phone      VARCHAR(15),
    address    TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP

);

-- Table 2: courses
CREATE TABLE IF NOT EXISTS courses (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    description  TEXT,
    duration     VARCHAR(50),
    fees         DECIMAL(10,2),
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP

);

-- Table 3: Enrollments
CREATE TABLE IF NOT EXISTS enrollments(
    id           INT AUTO_INCREMENT PRIMARY KEY,
    student_id   INT NOT NULL,
    course_id    INT NOT NULL,
    enroll_date  DATE DEFAULT (CURRENT_DATE),
    status       ENUM('active','completed','droped') DEFAULT 'active',
    grade        VARCHAR(5),
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
    UNIQUE KEY unique_enrollment (student_id,course_id)

);

INSERT INTO students (name,email,phone,address) VALUES
('Rahul Sharma','rahul@example.com','9876543210','Delhi'),
('Priya Verma','priya@example.com','8756432109','Mumbai'),
('Amit Das','amit@example.com','7654321098','Kolkata');

INSERT INTO courses (name,description,duration,fees) VALUES
('python programming','Learn python from scratch','3 months',4999.00),
('Wed Development','HTML,CSS,JS,Flask','4 months',7999.00),
('MYSQL Database','Database design and SQL','2 months',3999.00);

INSERT INTO enrollments (student_id,course_id,status) VALUES
(1,1,'active'),
(1,2,'active'),
(2,1,'completed'),
(3,3,'active');
-- USE student_management;
-- SELECT * FROM students;
USE student_management;
SELECT * FROM courses;
USE student_management;

INSERT INTO courses (name, description, duration, fees) VALUES
('Python Programming', 'Learn Python from scratch', '3 months', 4999.00),
('Web Development', 'HTML, CSS, JS, Flask', '4 months', 7999.00),
('MySQL Database', 'Database design and SQL', '2 months', 3999.00);

INSERT INTO enrollments (student_id, course_id, status) VALUES
(1, 1, 'active'),
(1, 2, 'active'),
(2, 1, 'completed'),
(3, 3, 'active');
USE student_management;
DELETE FROM enrollments;
DELETE FROM courses;
DELETE FROM students;
ALTER TABLE students AUTO_INCREMENT = 1;
ALTER TABLE courses AUTO_INCREMENT = 1;
ALTER TABLE enrollments AUTO_INCREMENT = 1;

INSERT INTO students (name, email, phone, address) VALUES
('Rahul Sharma', 'rahul@example.com', '9876543210', 'Delhi'),
('Priya Verma', 'priya@example.com', '8756432109', 'Mumbai'),
('Amit Das', 'amit@example.com', '7654321098', 'Kolkata');

INSERT INTO courses (name, description, duration, fees) VALUES
('Python Programming', 'Learn Python from scratch', '3 months', 4999),
('Web Development', 'HTML CSS Flask MySQL', '4 months', 7999),
('MySQL Database', 'Database design and SQL', '2 months', 3999);

INSERT INTO enrollments (student_id, course_id, status) VALUES
(1, 1, 'active'),
(1, 2, 'active'),
(2, 1, 'completed'),
(3, 3, 'active');


-- Add to your existing database.sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert a default admin user (password: admin123)
INSERT INTO users (username, password_hash, email) 
VALUES ('admin', 'scrypt:32768:8:1$...', 'admin@example.com');
-- Note: You'll create password hash using Python, not directly in SQL
USE student_management;
SELECT * FROM students;
INSERT INTO students (name, email, phone, address) VALUES
('Alice Johnson', 'alice@email.com', '9876543210', 'Delhi'),
('Bob Smith',    'bob@email.com',   '9123456780', 'Mumbai'),
('Carol White',  'carol@email.com', '9012345678', 'Kolkata');