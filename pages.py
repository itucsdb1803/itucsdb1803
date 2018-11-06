from werkzeug.utils import redirect
from database import DatabaseOperations
from flask import Blueprint, render_template, request, url_for
from login import LoginDatabase


site = Blueprint('site', __name__,)


@site.route('/initdb')
def initialize_database():
    database = DatabaseOperations()
    database.create_tables()
    database.init_db()
    return "Database initialized!"


@site.route('/')
def home_page():
    return render_template("home.html")


@site.route("/login", methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        ld = LoginDatabase()
        loginInfo = ld.log_in_job(username=request.form['username'], password=request.form['password'])
        if loginInfo is None or loginInfo == -1:
            error = 'Invalid Credentials. Please try again.'
        else:
            #login_user(loginInfo)
            return redirect(url_for('site.home_page'))
    return render_template('login.html', error=error)
