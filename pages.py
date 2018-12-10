from werkzeug.utils import redirect
from database import DatabaseOperations
from flask import Blueprint, render_template, request, url_for
from login import LoginDatabase
from flask_login import login_user, logout_user
from personal import PersonalDatabase
from disease import DiseaseDatabase
from hospital import HospitalDatabase
from department import DepartmentDatabase
from room import RoomDatabase


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
            login_user(loginInfo)
            return redirect(url_for('site.home_page'))
    return render_template('login.html', error=error)

@site.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@site.route('/personal')
def personel_page():
    personal = PersonalDatabase()
    personal.add_personal(1, 1, 1, 1, 1, 1, 1, "Utku", "Anıl", "16.01.1995")
    return render_template("home.html")

@site.route('/disease',methods=['GET', 'POST'])
def disease_page():
    derror = "OK"
    if request.method=='POST':
        disease = DiseaseDatabase()
        diseaseAddCheck = disease.add_disease(department=request.form['departmentid'],name=request.form['namer'],diseasearea=request.form['diseasearea'],description=request.form['description'])
        if diseaseAddCheck is None or diseaseAddCheck==-1:
            derror = 'Disease could not be added.'
        else:
            derror = 'Disease is added'
        return render_template("disease.html", derror=derror)
    else:
        return render_template("disease.html")

@site.route('/hospital')
def hospital_page():
    hospital = HospitalDatabase()
    hospital.add_hospital(1, 1, 1, 1, "Orhan")
    return render_template("home.html")

@site.route('/department')
def department_page():
    department = DepartmentDatabase()
    department.add_department(1, 1, 1, 1, 1, 1)
    return render_template("home.html")

@site.route('/room')
def room_page():
    room = RoomDatabase()
    room.add_room(1, 1, 1, 1, 1)
    return render_template("home.html")