from werkzeug.utils import redirect
from database import DatabaseOperations
from flask import Blueprint, render_template, request, url_for
from login import LoginDatabase
from flask_login import login_user, logout_user, current_user
from personal import PersonalDatabase
from disease import DiseaseDatabase
from hospital import HospitalDatabase
from department import DepartmentDatabase
from room import RoomDatabase
from parameter import ParameterDatabase
from duty import DutyDatabase
from parameter_type import ParameterTypeDatabase
from patient import PatientDatabase
from medicalreport import MedicalReportDatabase
from Reservation import ReservationDatabase


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


@site.route('/disease', methods=['GET', 'POST'])
def disease_page():
    derror = "OK"
    if request.method=='POST':
        disease = DiseaseDatabase()
        diseaseAddCheck = disease.add_disease(department=request.form['departmentid'],name=request.form['namer'],diseasearea=request.form['diseasearea'],description=request.form['description'])
        if diseaseAddCheck is None or diseaseAddCheck == -1:
            derror = 'Disease could not be added.'
        else:
            derror = 'Disease is added'
        return render_template("disease.html", derror=derror)
    else:
        return render_template("disease.html")

@site.route('/medicalreport', methods=['GET', 'POST'])
def medicalreport_page():
    derror = "OK"
    if request.method=='POST':
        the_report = MedicalReportDatabase()
        reportAddCheck = the_report.add_report(patientid=request.form['patientid'], doctorid=request.form['doctorid'], diseaseid=request.form['diseaseid'], treatment=request.form['treatment'], prescription=request.form['prescription'], report=request.form['report'])
        if reportAddCheck is None or reportAddCheck == -1:
            derror = 'Report could not be added.'
        else:
            derror = 'Report is added'
        return render_template("medicalreport.html", derror=derror)
    else:
        return render_template("medicalreport.html")

@site.route('/reservation', methods=['GET', 'POST'])
def reservation_page():
    derror = "OK"
    if request.method=='POST':
        make_reservation = ReservationDatabase()
        reservationAddCheck = make_reservation.add_reservation(patientid=request.form['patientid'], hospitalid=request.form['hospitalid'], doctorid=request.form['doctorid'], departmentid=request.form['departmentid'],
                                                                diseaseid=request.form['diseaseid'], comment=request.form['comment'], reservationdate=request.form['reservationdate'], reservationhour=request.form['reservationhour'])
        if reservationAddCheck is None or reservationAddCheck == -1:
            derror = 'Reservation could not be added.'
        else:
            derror = 'Reservation is done'
        return render_template("reservation.html", derror=derror)
    else:
        return render_template("reservation.html")

@site.route('/hospital', methods=['GET', 'POST'])
def hospital_page():
    derror = "OK"
    if request.method=='POST':
        hospital = HospitalDatabase()
        hospitalAddCheck = hospital.add_hospital(city=request.form['City'], capacity=request.form['Capacity'], address=request.form['Address'], name=request.form['Name'])

        if hospitalAddCheck is None or hospitalAddCheck == -1:
            derror = 'Hospital could not be opened'
        else:
            derror = 'Hospital is added'
        return render_template("hospital.html", derror=derror)
    else:
        return render_template("hospital.html")


@site.route('/department/<int:DepartmentID>')
def department_page(DepartmentID):
    department = DepartmentDatabase()
    department = department.get_department_info(DepartmentID)
    return render_template("department.html", department=department)


@site.route('/room/<int:RoomID>')
def room_page(RoomID):
    room = RoomDatabase()
    room = room.get_room_info(RoomID)
    return render_template("room.html", room=room)


@site.route('/personal/<int:UserID>')
def personel_page(UserID):
    personal = PersonalDatabase()
    profile = personal.get_profile_info(UserID)
    return render_template("personal.html", profile=profile)


@site.route('/register/personal' , methods=['GET', 'POST'])
def register_personal_page():
    if request.method == 'POST':
        personal = PersonalDatabase()
        login = LoginDatabase()

        username = request.form['UserName']
        password = request.form['Password']
        isUsernameValid = login.username_validator(username)
        if isUsernameValid:
            login.add_login(username=username, password=password, isEmployee="true")
            loginInfo = login.select_login_info(None, username, password)

            personal.add_personal(loginInfo.get_id(), hospitalID=request.form['HospitalID'],
                                departmentID=request.form['DepartmentID'], createUserID=current_user.id,
                                userType=request.form['UserType'], regNu=request.form['RegNu'], telNo=request.form['TelNo'],
                                name=request.form['Name'], surname=request.form['Surname'], birthDay=request.form['Birthday'],
                                birthPlace = request.form['BirthPlace'])
            return redirect(url_for('site.home_page'))
        else:
            return redirect(url_for('site.home_page'))
    else:
        parameter = ParameterDatabase()
        userTypes = parameter.select_parameters_with_type(2)
        cities = parameter.select_parameters_with_type(1)
        hospitals = [(1, 2, "Örnek Hastane")]
        departments = parameter.select_parameters_with_type(3)
        return render_template("personal_register.html", userTypes = userTypes, cities = cities, hospitals = hospitals, departments = departments)


@site.route('/personal/update/<int:UserID>' , methods=['GET', 'POST'])
def update_personal_page(UserID):
    if request.method == 'POST':
        personal = PersonalDatabase()
        login = LoginDatabase()

        password = request.form['Password']
        if password is not None and password != '':
            login.change_password(UserID, password)

        personal.update_personal(userID=UserID, hospitalID=request.form['HospitalID'],
                                 departmentID=request.form['DepartmentID'], userType=request.form['UserType'],
                                 regNu=request.form['RegNu'], name=request.form['Name'], telNo=request.form['TelNo'],
                                 surname=request.form['Surname'], birthDay=request.form['Birthday'],
                                 birthPlace=request.form['BirthPlace'])
        return redirect(url_for('site.home_page'))
    else:
        parameter = ParameterDatabase()
        personal = PersonalDatabase()
        personalInfo = personal.select_personal_info(UserID)
        userTypes = parameter.select_parameters_with_type(2)
        cities = parameter.select_parameters_with_type(1)
        hospitals = [(1, 2, "Örnek Hastane")]
        departments = parameter.select_parameters_with_type(3)
        return render_template("personal_update.html", userTypes=userTypes, cities=cities, hospitals=hospitals, departments=departments, personal=personalInfo)


@site.route('/duty', methods=['GET', 'POST'])
def duty_page():
    if request.method == 'POST':
        deletes = request.form.getlist('duty_to_delete')
        duty = DutyDatabase()
        for delete in deletes:
            duty.delete_duty_info(delete)
        return redirect(url_for('site.duty_page'))
    else:
        duty = DutyDatabase()
        dutyList = duty.select_all_duty_info()
        return render_template("duty.html", dutyList=dutyList)



@site.route('/duty/add', methods=['GET', 'POST'])
def duty_add_page():
    if request.method == 'POST':
        duty = DutyDatabase()
        duty.add_duty(doctorID=current_user.id, patientCount=request.form['PatientCount'], report=request.form['Report'], shiftDate=request.form['ShiftDate'])
        return redirect(url_for('site.duty_page'))
    else:
        return render_template("duty_add.html")


@site.route('/duty/update/<int:DutyID>', methods=['GET', 'POST'])
def duty_update_page(DutyID):
    if request.method == 'POST':
        duty = DutyDatabase()
        duty.update_duty(dutyID=DutyID, patientCount=request.form['PatientCount'], report=request.form['Report'], shiftDate=request.form['ShiftDate'])
        return redirect(url_for('site.duty_page'))
    else:
        duty = DutyDatabase()
        dutyInfo = duty.select_duty_info(DutyID)
        return render_template("duty_update.html", dutyInfo=dutyInfo)


@site.route('/parameter' , methods=['GET', 'POST'])
def parameter_page():
    if request.method == 'POST':
        return redirect(url_for('site.home_page'))
    else:
        return render_template("site.home_page")


@site.route('/parameter/add' , methods=['GET', 'POST'])
def parameter_add_page():
    if request.method == 'POST':
        parameter = ParameterDatabase()
        parameter.add_parameter(name=request.form['Name'], typeID=request.form['Type'])
        return redirect(url_for('site.home_page'))
    else:
        parameterTypes = ParameterTypeDatabase()
        parameters = parameterTypes.select_parameter_types()
        return render_template("parameter_add.html", parameters=parameters)


@site.route('/patient/<int:UserID>')
def patient_page(UserID):
    patient = PatientDatabase()
    profile = patient.get_profile_info(UserID)
    return render_template("patient.html", profile=profile)


@site.route('/register/patient', methods=['GET', 'POST'])
def register_patient_page():
    if request.method == 'POST':
        patient = PatientDatabase()
        login = LoginDatabase()

        username = request.form['UserName']
        password = request.form['Password']
        isUsernameValid = login.username_validator(username)
        if isUsernameValid:
            login.add_login(username=username, password=password, isEmployee="false")
            loginInfo = login.select_login_info(None, username, password)
            patient.add_patient(patientId=loginInfo.get_id(), createUserID=current_user.id, tckn=request.form['TCKN'],
                                gsm=request.form['GSM'], name=request.form['Name'],
                                surname=request.form['Surname'], birthDay=request.form['Birthday'],
                                birthPlace=request.form['BirthPlace'])
            return redirect(url_for('site.home_page'))
        else:
            return redirect(url_for('error.html'))
    else:
        parameter = ParameterDatabase()
        cities = parameter.select_parameters_with_type(1)
        return render_template("patient_register.html", cities=cities)


@site.route('/patient/update/<int:UserID>', methods=['GET', 'POST'])
def update_patient_page(UserID):
    if request.method == 'POST':
        patient = PatientDatabase()
        login = LoginDatabase()

        password = request.form['Password']
        if password is not None and password != '':
            login.change_password(UserID, password)

        patient.update_patient(patientId=UserID, tckn=request.form['TCKN'], birthPlace=request.form['BirthPlace'],
                               gsm=request.form['GSM'], name=request.form['Name'], surname=request.form['Surname'],
                               birthDay=request.form['Birthday'])

        return redirect(url_for('site.home_page'))
    else:
        parameter = ParameterDatabase()
        patient = PatientDatabase()
        patientInfo = patient.select_patient_info(UserID)
        cities = parameter.select_parameters_with_type(1)
        return render_template("patient_update.html",  cities=cities, patient=patientInfo)


@site.route('/search', methods=['GET', 'POST'])
def search_page():
    if request.method == 'POST':
        login = LoginDatabase()
        search = login.user_search(username=request.form['username'], name=request.form['name'],
                                   surname=request.form['surname'], isEmployee=request.form['Type'])
        return search_result_page(search)
    else:
        return render_template("search.html")


@site.route('/search/result', methods=['GET', 'POST'])
def search_result_page(search):
    return render_template("search.html", searchList=search)


@site.route('/register', methods=['GET', 'POST'])
def register_page():
    return render_template("register.html")