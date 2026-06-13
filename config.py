# import os

# class Config:
#     MYSQL_HOST = os.environ.get('MYSQL_HOST', 'thomas.proxy.rlwy.net')
#     MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
#     MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'naba@123')
#     MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'railway')
#     MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
#     SECRET_KEY = os.environ.get('SECRET_KEY', 'abc@nfkhhokokjmjhgbiugiioj9ypujidj98uipuju')
#     DEBUG = os.environ.get('DEBUG', 'False') == 'True'
import os
class Config:
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'naba@123')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'student_management')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'naba@kfvjihhoiojdkhyudgihhgygy')
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'