from database import DatabaseOperations

def initialize_database():
    database = DatabaseOperations()
    database.create_tables()
    return "Database initialized!"

def home_page():
    return "Hello World!"

def login_page():
    return "Hello to Login Page!"