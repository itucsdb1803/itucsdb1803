from server import *
from server import app
from database import DatabaseOperations

@app.route('/initdb')
def initialize_database():
    database = DatabaseOperations()
    database.create_tables()
    return "Database initialized!"

@app.route("/")
@app.route("/index")
def home_page():
    return "Hello World!"


@app.route("/login")
def login_page():
    return "Hello to Login Page!"