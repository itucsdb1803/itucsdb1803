from werkzeug.utils import redirect
from database import DatabaseOperations
from flask import Blueprint, render_template, request, url_for
from login import LoginDatabase
from flask_login import login_user, logout_user, current_user, login_required
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
    return redirect(url_for('site.login_page'))


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
            if str(current_user.IsEmployee) == "True":
                return personel_page(current_user.id)
            else:
                return patient_page(current_user.id)
    return render_template('login.html', error=error)


@site.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.login_page'))


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

@site.route('/updatereservation/<int:ReservationID>')
def updatereservation_page(ReservationID):
    derror = "OK"
    if request.method=='POST':
        make_reservation = ReservationDatabase()
        reservationAddCheck = make_reservation.update_reservation(reservationid=ReservationID, patientid=request.form['patientid'], hospitalid=request.form['hospitalid'], doctorid=request.form['doctorid'], departmentid=request.form['departmentid'],
                                                                diseaseid=request.form['diseaseid'], comment=request.form['comment'], reservationdate=request.form['reservationdate'], reservationhour=request.form['reservationhour'])
        if reservationAddCheck is None or reservationAddCheck == -1:
            derror = 'Reservation could not be updated.'
        else:
            derror = 'Reservation is updated'
        return render_template("updatereservation.html", derror=derror)
    else:
        return render_template("updatereservation.html")

@site.route('/hospital', methods=['GET', 'POST'])
def hospital_page():
    derror = "OK"
    if request.method=='POST':
        hospital = HospitalDatabase()
        hospitalAddCheck = hospital.add_hospital(city=request.form['City'], capacity=request.form['Capacity'], address=request.form['Address'], name=request.form['Name'])

        if hospitalAddCheck is None or hospitalAddCheck == -1:
            derror = 'Hospital could not be added'
        else:
            derror = 'Hospital is added'
        return render_template("hospital.html", derror=derror)
    else:
        return render_template("hospital.html")

@site.route('/updatehospital/<int:HospitalID>')
def updaterehospital_page(HospitalID):
    derror = "OK"
    if request.method=='POST':
        create_hospital = HospitalDatabase()
        hospitalAddCheck = create_hospital.update_hospital(hospitalid=HospitalID, city=request.form['City'], capacity=request.form['Capacity'], address=request.form['Address'], name=request.form['Name'])
        if hospitalAddCheck is None or hospitalAddCheck == -1:
            derror = 'Hospital info could not be updated.'
        else:
            derror = 'Hospital info is updated'
        return render_template("updatehospital.html", derror=derror)
    else:
        return render_template("updatehospital.html")

@site.route('/department', methods=['GET', 'POST'])
def department_page():
    derror = "OK"
    if request.method=='POST':
        department = DepartmentDatabase()
        departmentAddCheck = department.add_department(hospitalid=request.form['HospitalID'], deptypeid=request.form['DepartmentTypeID'], roomcount=request.form['RoomCount'], blocknumber=request.form['BlockNumber'], personalcount=request.form['PersonalCount'])

        if departmentAddCheck is None or departmentAddCheck == -1:
            derror = 'Department could not be added'
        else:
            derror = 'Department is added'
        return render_template("department.html", derror=derror)
    else:
        return render_template("department.html")

@site.route('/updatedepartment/<int:DepartmentID>')
def updatedepartment_page(DepartmentID):
    derror = "OK"
    if request.method=='POST':
        create_department = DepartmentDatabase()
        departmentAddCheck = create_department.update_department(departmentid=DepartmentID, hospitalid=request.form['HospitalID'], departmentTypeid=request.form['DepartmentTypeID'], roomCount=request.form['RoomCount'], blockNumber=request.form['BlockNumber'], personalCount=request.form['PersonalCount'])
        if departmentAddCheck is None or departmentAddCheck == -1:
            derror = 'Department info could not be updated.'
        else:
            derror = 'Department info is updated'
        return render_template("updatedepartment.html", derror=derror)
    else:
        return render_template("updatedepartment.html")

@site.route('/room', methods=['GET', 'POST'])
def room_page():
    derror = "OK"
    if request.method=='POST':
        room = RoomDatabase()
        roomAddCheck = room.add_room(departmentid=request.form['DepartmentID'], roomno=request.form['RoomNo'], capacity=request.form['Capacity'], bathroomcount=request.form['BathroomCount'])

        if roomAddCheck is None or roomAddCheck == -1:
            derror = 'Room could not be added'
        else:
            derror = 'Room is added'
        return render_template("room.html", derror=derror)
    else:
        return render_template("room.html")

@site.route('/updateroom/<int:RoomID>')
def updateredepartment_page(RoomID):
    derror = "OK"
    if request.method=='POST':
        create_room = RoomDatabase()
        roomAddCheck = create_room.update_room(roomid=RoomID, departmentid=request.form['DepartmentID'], roomno=request.form['RoomNo'], capacity=request.form['Capacity'], bathroomCount=request.form['BathroomCount'])
        if roomAddCheck is None or roomAddCheck == -1:
            derror = 'Room info could not be updated.'
        else:
            derror = 'Room info is updated'
        return render_template("updateroom.html", derror=derror)
    else:
        return render_template("updateroom.html")


@site.route('/personal/<int:UserID>')
@login_required
def personel_page(UserID):
    if str(current_user.IsEmployee) == "True":
        personal = PersonalDatabase()
        profile = personal.get_profile_info(UserID)
        return render_template("personal.html", profile=profile)
    else:
        return render_template("permission_denied.html")

@site.route('/register/personal' , methods=['GET', 'POST'])
@login_required
def register_personal_page():
    if str(current_user.IsEmployee) == "True":
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
                return redirect(url_for('site.profile_page'))
            else:
                return render_template("error.html")
        else:
            parameter = ParameterDatabase()
            hospital = HospitalDatabase()
            userTypes = parameter.select_parameters_with_type(2)
            cities = parameter.select_parameters_with_type(1)
            hospitals = hospital.select_all_hospital_info("")
            departments = parameter.select_parameters_with_type(3)
            return render_template("personal_register.html", userTypes = userTypes, cities = cities, hospitals = hospitals, departments = departments)
    else:
        return render_template("permission_denied.html")


@site.route('/personal/update/<int:UserID>' , methods=['GET', 'POST'])
@login_required
def update_personal_page(UserID):
    if str(current_user.IsEmployee) == "True":
        if request.method == 'POST':
            personal = PersonalDatabase()
            login = LoginDatabase()

            password = request.form['Password']
            if password is not None and password != '':
                login.change_password(UserID, password)

            personal.update_personal(userID=UserID, hospitalID=request.form.get("HospitalID", None),
                                     departmentID=request.form.get("DepartmentID", None), userType=request.form.get("UserType", None),
                                     regNu=request.form['RegNu'], name=request.form['Name'], telNo=request.form['TelNo'],
                                     surname=request.form['Surname'], birthDay=request.form['Birthday'],
                                     birthPlace=request.form.get("BirthPlace", None))
            return redirect(url_for('site.profile_page'))
        else:
            parameter = ParameterDatabase()
            personal = PersonalDatabase()
            hospital = HospitalDatabase()
            personalInfo = personal.select_personal_info(UserID)
            userTypes = parameter.select_parameters_with_type(2)
            cities = parameter.select_parameters_with_type(1)
            hospitals = hospital.select_all_hospital_info(None)
            departments = parameter.select_parameters_with_type(3)
            return render_template("personal_update.html", userTypes=userTypes, cities=cities, hospitals=hospitals, departments=departments, personal=personalInfo)
    else:
        return render_template("permission_denied.html")


@site.route('/duty', methods=['GET', 'POST'])
@login_required
def duty_page():
    if str(current_user.IsEmployee) == "True":
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
    else:
        return render_template("permission_denied.html")


@site.route('/duty/add', methods=['GET', 'POST'])
@login_required
def duty_add_page():
    if str(current_user.IsEmployee) == "True":
        if request.method == 'POST':
            duty = DutyDatabase()
            duty.add_duty(doctorID=current_user.id, patientCount=request.form['PatientCount'], report=request.form['Report'], shiftDate=request.form['ShiftDate'])
            return redirect(url_for('site.duty_page'))
        else:
            return render_template("duty_add.html")
    else:
        return render_template("permission_denied.html")


@site.route('/duty/update/<int:DutyID>', methods=['GET', 'POST'])
@login_required
def duty_update_page(DutyID):
    if str(current_user.IsEmployee) == "True":
        if request.method == 'POST':
            duty = DutyDatabase()
            duty.update_duty(dutyID=DutyID, patientCount=request.form['PatientCount'], report=request.form['Report'], shiftDate=request.form['ShiftDate'])
            return redirect(url_for('site.duty_page'))
        else:
            duty = DutyDatabase()
            dutyInfo = duty.select_duty_info(DutyID)
            return render_template("duty_update.html", dutyInfo=dutyInfo)
    else:
        return render_template("permission_denied.html")


@site.route('/parameter' , methods=['GET', 'POST'])
@login_required
def parameter_page():
    if str(current_user.IsEmployee) == "True":
        if request.method == 'POST':
            return redirect(url_for('site.profile_page'))
        else:
            return render_template("site.profile_page")
    else:
        return render_template("permission_denied.html")


@site.route('/parameter/add' , methods=['GET', 'POST'])
@login_required
def parameter_add_page():
    if str(current_user.IsEmployee) == "True":
        if request.method == 'POST':
            parameter = ParameterDatabase()
            parameter.add_parameter(name=request.form['Name'], typeID=request.form['Type'])
            return redirect(url_for('site.profile_page'))
        else:
            parameterTypes = ParameterTypeDatabase()
            parameters = parameterTypes.select_parameter_types()
            return render_template("parameter_add.html", parameters=parameters)
    else:
        return render_template("permission_denied.html")


@site.route('/patient/<int:UserID>')
@login_required
def patient_page(UserID):
    patient = PatientDatabase()
    profile = patient.get_profile_info(UserID)
    reservation = ReservationDatabase()
    reservation_list = reservation.select_reservation_info(UserID)
    return render_template("patient.html", profile=profile, reservation=reservation_list)


@site.route('/register/patient', methods=['GET', 'POST'])
@login_required
def register_patient_page():
    if str(current_user.IsEmployee) == "True":
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
                                    birthPlace=request.form.get("BirthPlace", None))
                return redirect(url_for('site.profile_page'))
            else:
                return render_template('error.html')
        else:
            parameter = ParameterDatabase()
            cities = parameter.select_parameters_with_type(1)
            return render_template("patient_register.html", cities=cities)
    else:
        return render_template("permission_denied.html")


@site.route('/patient/update/<int:UserID>', methods=['GET', 'POST'])
@login_required
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

            return redirect(url_for('site.profile_page'))
        else:
            parameter = ParameterDatabase()
            patient = PatientDatabase()
            patientInfo = patient.select_patient_info(UserID)
            cities = parameter.select_parameters_with_type(1)
            return render_template("patient_update.html",  cities=cities, patient=patientInfo)


@site.route('/search', methods=['GET', 'POST'])
@login_required
def search_page():
    if str(current_user.IsEmployee) == "True":
        if request.method == 'POST':
            login = LoginDatabase()
            search = login.user_search(username=request.form['username'], name=request.form['name'],
                                       surname=request.form['surname'], isEmployee=request.form['Type'])
            return search_result_page(search)
        else:
            return render_template("search.html")
    else:
        return render_template("permission_denied.html")


@site.route('/search/result', methods=['GET', 'POST'])
@login_required
def search_result_page(search):
    if str(current_user.IsEmployee) == "True":
        return render_template("search.html", searchList=search)
    else:
        return render_template("permission_denied.html")


@site.route('/register', methods=['GET', 'POST'])
@login_required
def register_page():
    if str(current_user.IsEmployee) == "True":
        return render_template("register.html")
    else:
        return render_template("permission_denied.html")


@site.route('/profile')
@login_required
def profile_page():
    if str(current_user.IsEmployee) == "True":
        return personel_page(current_user.id)
    else:
        return patient_page(current_user.id)