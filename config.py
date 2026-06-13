class Config:
    # Database Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'naba@123'  # Your password
    MYSQL_DATABASE = 'student_management'
    
    # Secret key for sessions
    SECRET_KEY = 'your-secret-key-here-change-this-to-something-random'
    
    # Other configurations
    DEBUG = True