from database import DatabaseOperations
from flask import Blueprint, render_template


site = Blueprint('site', __name__,)


@site.route('/initdb')
def initialize_database():
    database = DatabaseOperations()
    database.create_tables()
    return "Database initialized!"


@site.route('/')
def home_page():
    return render_template("home.html")


@site.route("/login")
def login_page():
    return "Hello to Login Page!"