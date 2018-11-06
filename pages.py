from database import DatabaseOperations
from flask import render_template

def initialize_database():
    database = DatabaseOperations()
    database.create_tables()
    return "Database initialized!"

def home_page():
    return render_template("home.html")

def login_page():
    return "Hello to Login Page!"