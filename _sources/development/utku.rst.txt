Parts Implemented by Utku Anil Saykara
======================================

All tables are created in the create_tables function at database.py.

Initializing Parameters and First User
--------------------------------------

When the "/initdb" page is opened, create_tables function is executed and all tables will create. After that, the function init_db is executed and the parameter types are added to the "ParameterType" table first. After adding the parameter types, the necessary initial parameters are added using these types. These parameters are found in the dictionaries in the init_parameters.py file. Then the user login information for the first user is created in the "LogInfo" table. With this information generated, the administrator's information is entered in the "PersonalInfo" table.

.. code-block:: python

        def init_db(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO ParameterType(ID, Name) VALUES (%s, %s)"""
            cursor.execute(query, ("1", "City"))

            query = """INSERT INTO ParameterType(ID, Name) VALUES (%s, %s)"""
            cursor.execute(query, ("2", "Duty"))

            query = """INSERT INTO ParameterType(ID, Name) VALUES (%s, %s)"""
            cursor.execute(query, ("3", "Department Type"))

            query = """INSERT INTO ParameterInfo(TypeID, Name) VALUES (1, %(city)s)"""
            cursor.executemany(query, city_dict)

            query = """INSERT INTO ParameterInfo(TypeID, Name) VALUES (2, %(job)s)"""
            cursor.executemany(query, job_dict)

            query = """INSERT INTO ParameterInfo(TypeID, Name) VALUES (3, %(dep)s)"""
            cursor.executemany(query, dep_dict)

            query = """INSERT INTO HospitalInfo(City, Capacity, Address, Name, CreateDate) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (34, "1500", "Maslak", "Acibadem", datetime.datetime.now()))

            query = """INSERT INTO LogInfo(UserName, Password, IsEmployee, CreateDate) VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, ("admin", "12345", "true", datetime.datetime.now()))

            query = """INSERT INTO PersonalInfo(UserID, HospitalID, DepartmentID, createUserID, UserType, RegNu, TelNo, BirthPlace, Name, Surname, BirthDay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, ("1", "1", "103", "1", "87", "0", "0", "1", "admin", "admin", datetime.datetime.now()))


Login Information
-----------------

The information required for the user to login to the system is kept in the "LogInfo" table. This table was used as the primary key of the user's UserID. This table also keeps the user name and password. Also, whether the user is a staff member, the last entry date and the last password change date are kept in this table.

.. code-block:: python

    query = """DROP TABLE IF EXISTS LogInfo CASCADE """
    cursor.execute(query)
    query = """CREATE TABLE LogInfo (
                      UserID SERIAL PRIMARY KEY,
                      UserName VARCHAR(100) NOT NULL,
                      Password VARCHAR(100) NOT NULL,
                      IsEmployee Boolean NOT NULL,
                      LastLoginDate TIMESTAMP,
                      CreateDate TIMESTAMP NOT NULL,
                      UpdateDate TIMESTAMP)"""
    cursor.execute(query)


The Login class keeps some information of the user who is currently logged into the system. As shown in the following snippet, this information is: ID, user name, password, last login time, create date, update date and employee information.

.. code-block:: python

    class Login(UserMixin):
    def __init__(self, id, username, password, isEmployee, lastLoginDate, createDate, updateDate):
        self.id = id
        self.UserName = username
        self.Password = password
        self.IsEmployee = isEmployee
        self.LastLoginDate = lastLoginDate
        self.CreateDate = createDate
        self.UpdateDate = updateDate

When the user open the login page, he/she logs in by filling out the forms. The log_in_job function in the LoginDatabase class in the Login.py file compares the information entered to the form with the records. If there is a user with this name and its password matches, it updates the last entry time and performs user login with the login_user function of the Flask-Login library.

.. code-block:: python

    @site.route("/login", methods=['GET', 'POST'])
    def login
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

log_in_job function is given below.

.. code-block:: python

    def log_in_job(cls, username, password):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            logData = None

            query = """SELECT * FROM LogInfo WHERE Username = %s AND Password = %s"""
            try:
                cursor.execute(query, (str(username), str(password)))
                logData = cursor.fetchone()

                if logData:
                    LoginDatabase.update_last_login(logData[0])

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            if logData:
                return Login(id=logData[0], username=logData[1], password=logData[2], isEmployee=logData[3],
                         lastLoginDate=logData[4], createDate=logData[5], updateDate=logData[6])
            else:
                return -1

User Information
----------------

Personnel Information
^^^^^^^^^^^^^^^^^^^^^

The information of the personnel is kept in the "PersonalInfo" table. UserID was used as the primary key. During user registration, the serial key created in the "LogInfo" table has been added to this table as UserID and a "one-to-one" relationship has been created with the "LogInfo" table. HospitalID was used as the foreign key to take the hospital information from the "HospitalInfo" table. The DepartmentID was used as an foreign key to retrieve the department where the personnel work from the "ParameterInfo" table. CreateUserID has been used as an foreign key to find the person who created the user in "LogInfo" table. UserType was used as the external key to retrieve the user's task information from the "ParameterInfo" table. BirthPlace is used as an foreign key to take the user's birth location from the "ParameterInfo" table.

.. code-block:: python

    query = """DROP TABLE IF EXISTS PersonalInfo CASCADE """
    cursor.execute(query)
    query = """CREATE TABLE PersonalInfo (
                      UserID INT PRIMARY KEY,
                      HospitalID INT NOT NULL,
                      DepartmentID INT NOT NULL,
                      CreateUserID INT NOT NULL,
                      UserType INT NOT NULL,
                      RegNu INT NOT NULL,
                      BirthPlace INT NOT NULL,
                      TelNo VARCHAR(50) NOT NULL,
                      Name VARCHAR(100) NOT NULL,
                      Surname VARCHAR(100) NOT NULL,
                      BirthDay TIMESTAMP,
                      UpdateDate TIMESTAMP,
                      FOREIGN KEY (UserID) REFERENCES LogInfo(UserID) ON DELETE CASCADE,
                      FOREIGN KEY (CreateUserID) REFERENCES LogInfo(UserID) ON DELETE RESTRICT,
                      FOREIGN KEY (BirthPlace) REFERENCES ParameterInfo(ID) ON DELETE RESTRICT,
                      FOREIGN KEY (HospitalID) REFERENCES HospitalInfo(HospitalID) ON DELETE RESTRICT,
                      FOREIGN KEY (DepartmentID) REFERENCES ParameterInfo(ID) ON DELETE RESTRICT,
                      FOREIGN KEY (UserType) REFERENCES ParameterInfo(ID) ON DELETE RESTRICT)"""
    cursor.execute(query)

Patient Information
^^^^^^^^^^^^^^^^^^^

The information of the patient is kept in the "PatientInfo" table. PatientID was used as the primary key. During user registration, the serial key created in the "LogInfo" table has been added to this table as PatientID and a "one-to-one" relationship has been created with the "LogInfo" table. CreateUserID has been used as an foreign key to find the person who created the user in "LogInfo" table. BirthPlace is used as an foreign key to take the user's birth location from the "ParameterInfo" table.

.. code-block:: python

    query = """DROP TABLE  IF EXISTS PatientInfo CASCADE"""
    cursor.execute(query)
    query = """CREATE TABLE PatientInfo(
                      PatientID INT PRIMARY KEY,
                      CreateUserID INT NOT NULL,
                      BirthPlace INT NOT NULL,
                      GSM VARCHAR(50) NOT NULL,
                      TCKN VARCHAR(50) NOT NULL,
                      Name VARCHAR(100) NOT NULL,
                      Surname VARCHAR(100) NOT NULL,
                      BirthDay TIMESTAMP NOT NULL,
                      UpdateDate TIMESTAMP,
                      FOREIGN KEY (PatientID) REFERENCES LogInfo(UserID) ON DELETE CASCADE,
                      FOREIGN KEY (CreateUserID) REFERENCES LogInfo(UserID) ON DELETE RESTRICT,
                      FOREIGN KEY (BirthPlace) REFERENCES ParameterInfo(ID) ON DELETE RESTRICT)"""
    cursor.execute(query)


User Profile
------------

Personnel Profile
^^^^^^^^^^^^^^^^^

The personnel profile can be viewed through this page. The get_profile_info function retrieves the user's information.

.. code-block:: python

    @login_required
    def personel_page(UserID):
        if str(current_user.IsEmployee) == "True":
            personal = PersonalDatabase()
            profile = personal.get_profile_info(UserID)
            return render_template("personal.html", profile=profile)
        else:
            return render_template("permission_denied.html")


The profile information of the personnel is retrieved with the get_profile_info function. When taking data from the database, appropriate data is retrieved using database relationships to see the values that correspond to those IDs instead of IDs. The user's age is calculated by taking the birthday information from the incoming data.

.. code-block:: python

    def get_profile_info(cls, userID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            personalInfo = None

            query = """SELECT p.UserID, l.username, p.Name, p.Surname, para2.Name, h.name, para1.name, p.RegNu, p.BirthDay, para3.Name, p.TelNo
                    FROM PersonalInfo p, ParameterInfo para1, ParameterInfo para2, ParameterInfo para3, HospitalInfo h, LogInfo l
                        WHERE p.DepartmentID = para1.ID AND p.UserType = para2.ID AND p.BirthPlace = para3.ID AND p.HospitalID = h.HospitalID AND p.UserID = l.UserID
                            AND p.UserID = %s"""
            try:
                cursor.execute(query, str(userID))
                personalInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if personalInfo:
                birthDay = personalInfo[8]
                today = datetime.datetime.now()
                age = int((today - birthDay).days / 365)
                profileInfo = [personalInfo[0], personalInfo[1], personalInfo[2], personalInfo[3], personalInfo[4],
                                personalInfo[5], personalInfo[6], personalInfo[7], age, personalInfo[9], personalInfo[10]]
                return profileInfo
            else:
                return []


Patient Profile
^^^^^^^^^^^^^^^

The patient profile can be viewed through this page. The get_profile_info function retrieves the user's information.


.. code-block:: python

    @login_required
    def patient_page(UserID):
        patient = PatientDatabase()
        profile = patient.get_profile_info(UserID)
        reservation = ReservationDatabase()
        reservation_list = reservation.select_reservation_info(UserID)
        return render_template("patient.html", profile=profile, reservation=reservation_list)


The profile information of the patient is retrieved with the get_profile_info function. When taking data from the database, appropriate data is retrieved using database relationships to see the values that correspond to those IDs instead of IDs. The user's age is calculated by taking the birthday information from the incoming data.


.. code-block:: python

    def get_profile_info(cls, patientID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            patientInfo = None

            query = """SELECT p.PatientID, l.username, p.name, p.Surname, p.TCKN, p.GSM, p.BirthDay, para.name
                FROM PatientInfo p, ParameterInfo para, LogInfo l
                WHERE p.BirthPlace = para.ID AND p.PatientID = l.UserID
                AND p.PatientID = %s"""
            try:
                cursor.execute(query, str(patientID))
                patientInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if patientInfo:
                birthDay = patientInfo[6]
                today = datetime.datetime.now()
                age = int((today - birthDay).days / 365)
                profileInfo = [patientInfo[0], patientInfo[1], patientInfo[2], patientInfo[3], patientInfo[4],
                               patientInfo[5], age, patientInfo[7]]
                return profileInfo
            else:
                return []



User Registration
-----------------

Personnel Registration
^^^^^^^^^^^^^^^^^^^^^^

First, the user's authorization is checked, if not authorized, the permission denied page is called. If it has permission, the username_validator function checks the availability of the user name that the user entered. If not, it will be redirected to the error page. If appropriate, the login information of the user is registered with the add_login function. After this recording is done, userID is selected with select_login_info function. Using the UserID, personnel information is entered using the add_personal function.

.. code-block:: python

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

username_validator is given below. username_validator function checks the availability of the user name.

.. code-block:: python

    def username_validator(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            logInfo = None

            query = "SELECT COUNT(*) FROM LogInfo WHERE username = %s" % (str("'" + username + "'"))
            try:
                cursor.execute(query)
                logInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if logInfo[0] == 0:
                return True
            else:
                return False


To add login information to "LogInfo" table, add_login function is used and add_login function is given below.

.. code-block:: python

    def add_login(cls, username, password, isEmployee):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO LogInfo(UserName, Password, isEmployee, CreateDate) VALUES (%s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(username), str(password), str(isEmployee), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()


To add personnel to "PersonalInfo" table, add_personal function is used and add_personal function is given below.

.. code-block:: python

    def add_personal(cls, UserID, hospitalID, departmentID, createUserID, userType, regNu, telNo, birthPlace, name, surname, birthDay):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PersonalInfo(UserID, HospitalID, DepartmentID, createUserID, UserType, RegNu, TelNo, BirthPlace, Name, Surname, BirthDay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(UserID), str(hospitalID), str(departmentID), str(createUserID), str(userType), str(regNu), str(telNo), str(birthPlace), str(name), str(surname), str(birthDay)))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return




Patient Registration
^^^^^^^^^^^^^^^^^^^^

First, the user's authorization is checked, if not authorized, the permission denied page is called. If it has permission, the username_validator function checks the availability of the user name that the user entered. If not, it will be redirected to the error page. If appropriate, the login information of the user is registered with the add_login function. After this recording is done, userID is selected with select_login_info function. Using the UserID, patient information is entered using the add_patient function.

.. code-block:: python

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

username_validator is given below. username_validator function checks the availability of the user name.

.. code-block:: python

    def username_validator(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            logInfo = None

            query = "SELECT COUNT(*) FROM LogInfo WHERE username = %s" % (str("'" + username + "'"))
            try:
                cursor.execute(query)
                logInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if logInfo[0] == 0:
                return True
            else:
                return False


To add login information to "LogInfo" table, add_login function is used and add_login function is given below.

.. code-block:: python

    def add_login(cls, username, password, isEmployee):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO LogInfo(UserName, Password, isEmployee, CreateDate) VALUES (%s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(username), str(password), str(isEmployee), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()


To add patient to "PatientInfo" table, add_patient function is used and add_patient function is given below.

.. code-block:: python

    def add_patient(cls, patientId, tckn, createUserID, birthPlace, gsm, name, surname, birthDay):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PatientInfo(PatientID, CreateUserID, TCKN, BirthPlace, GSM, Name, Surname, BirthDay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

            try:
                cursor.execute(query, (str(patientId), str(createUserID), str(tckn), str(birthPlace), str(gsm), str(name), str(surname), str(birthDay)))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return


User Update
-----------

Personnel Update
^^^^^^^^^^^^^^^^

The user's information is updated via the user number when the request to update the profile is received. If the user has entered a new password, the change_password function is called and the password is changed. Then the other information of the staff is updated via update_personal.

.. code-block:: python

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


change_password function is updating password of user. change_password function is given below.

.. code-block:: python

    def change_password(cls, userID, password):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            if password != '' and password is not None:
                query = """UPDATE LogInfo SET Password = '%s', UpdateDate = '%s' WHERE UserID = %s""" \
                        % (str(password), datetime.datetime.now(), str(userID))
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

update_personal function is updating information of personnel which is only changed by user. update_personal function is given below.

.. code-block:: python

    def update_personal(cls, userID, hospitalID, departmentID, userType, regNu, telNo, birthPlace, name, surname, birthDay):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = 'UPDATE PersonalInfo SET UpdateDate = ' + "'" + str(datetime.datetime.now()) + "'"

            if hospitalID != '' and hospitalID is not None:
                query = query + ", HospitalID = '" + str(hospitalID) + "'"
            if departmentID != '' and departmentID is not None:
                query = query + ", DepartmentID = '" + str(departmentID) + "'"
            if userType != '' and userType is not None:
                query = query + ", UserType = '" + str(userType) + "'"
            if regNu != '' and regNu is not None:
                query = query + ", RegNu = '" + str(regNu) + "'"
            if telNo != '' and telNo is not None:
                query = query + ", TelNo = '" + str(telNo) + "'"
            if birthPlace != '' and birthPlace is not None:
                query = query + ", BirthPlace = '" + str(birthPlace) + "'"
            if name != '' and name is not None:
                query = query + ", Name = '" + str(name) + "'"
            if surname != '' and surname is not None:
                query = query + ", Surname = '" + str(surname) + "'"
            if birthDay != '' and birthDay is not None:
                query = query + ", BirthDay = '" + str(birthDay) + "'"
            query = query + ' WHERE UserID = ' + str(userID)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

Patient Update
^^^^^^^^^^^^^^

The user's information is updated via the user number when the request to update the profile is received. If the user has entered a new password, the change_password function is called and the password is changed. Then the other information of the patient is updated via update_patient.

.. code-block:: python

    @login_required
    def update_patient_page(UserID):
        if request.method == 'POST':
            patient = PatientDatabase()
            login = LoginDatabase()

            password = request.form['Password']
            if password is not None and password != '':
                login.change_password(UserID, password)

            patient.update_patient(patientId=UserID, tckn=request.form['TCKN'], birthPlace=request.form.get("BirthPlace", None),
                                   gsm=request.form['GSM'], name=request.form['Name'], surname=request.form['Surname'],
                                   birthDay=request.form['Birthday'])

            return redirect(url_for('site.profile_page'))
        else:
            parameter = ParameterDatabase()
            patient = PatientDatabase()
            patientInfo = patient.select_patient_info(UserID)
            cities = parameter.select_parameters_with_type(1)
            return render_template("patient_update.html",  cities=cities, patient=patientInfo)

change_password function is updating password of user. change_password function is given below.

.. code-block:: python

    def change_password(cls, userID, password):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            if password != '' and password is not None:
                query = """UPDATE LogInfo SET Password = '%s', UpdateDate = '%s' WHERE UserID = %s""" \
                        % (str(password), datetime.datetime.now(), str(userID))
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

update_patient function is updating information of patient which is only changed by user. update_patient function is given below.

.. code-block:: python

    def update_patient(cls, patientId, tckn, birthPlace, gsm, name, surname, birthDay):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = 'UPDATE PatientInfo SET UpdateDate = ' + "'" + str(datetime.datetime.now()) + "'"

            if gsm != '' and gsm is not None:
                query = query + ", GSM = '" + str(gsm) + "'"
            if tckn != '' and tckn is not None:
                query = query + ", TCKN = '" + str(tckn) + "'"
            if birthPlace != '' and birthPlace is not None:
                query = query + ", BirthPlace = '" + str(birthPlace) + "'"
            if name != '' and name is not None:
                query = query + ", Name = '" + str(name) + "'"
            if surname != '' and surname is not None:
                query = query + ", Surname = '" + str(surname) + "'"
            if birthDay != '' and birthDay is not None:
                query = query + ", BirthDay = '" + str(birthDay) + "'"
            query = query + ' WHERE PatientId = ' + str(patientId)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

User Delete
-----------

Personnel Delete
^^^^^^^^^^^^^^^^

delete_personal_info is deleting information of personal.

.. code-block:: python

    def delete_personal_info(cls, userID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM PersonalInfo WHERE UserID = %s"""
            try:
                cursor.execute(query, (userID))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            return

Patient Delete
^^^^^^^^^^^^^^

delete_patient_info is deleting information of personal.

.. code-block:: python

        def delete_patient_info(cls, userID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM PatientInfo WHERE PatientID = %s"""
            try:
                cursor.execute(query, (userID))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            return

User Search
-----------

Returns the relevant results using the user_search function according to the data entered by the user.

.. code-block:: python

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


The user_search function only returns the required results using the information entered by the user. During the query, appropriate data is retrieved using database relationships to see the values that correspond to those IDs instead of IDs. user_search function is given below.

.. code-block:: python

        def user_search(cls, username, name, surname, isEmployee):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            logInfo = None
            query = "SELECT l.UserID, l.username, p.name, p.surname,"
            if isEmployee == "True":
                query = query + " par.name, p.TelNo FROM LogInfo l, personalInfo p, parameterInfo par WHERE l.UserID = p.UserID AND p.usertype = par.ID"
                if username is not None and username != "":
                    query = query + " AND l.username like '%" + username + "%'"
                if name is not None and name != "":
                    query = query + " AND p.name like '%" + name + "%'"
                if surname is not None and surname != "":
                    query = query + " AND p.surname like '%" + surname + "%'"
            else:
                query = query + "  p.GSM FROM LogInfo l, patientInfo p WHERE l.UserID = p.patientID"
                if username is not None and username != "":
                    query = query + " AND l.username like '%" + username + "%'"
                if name is not None and name != "":
                    query = query + " AND p.name like '%" + name + "%'"
                if surname is not None and surname != "":
                    query = query + " AND p.surname like '%" + surname + "%'"
            try:
                cursor.execute(query)
                logInfo = cursor.fetchall()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            result = []
            if logInfo:
                if isEmployee == "True":
                    for log in logInfo:
                        input = [log[0], log[1], log[2], log[3], log[4], log[5], "/personal/"]
                        result.append(input)
                    return result
                else:
                    for log in logInfo:
                        input = [log[0], log[1], log[2], log[3], log[4], "Patient", "/patient/"]
                        result.append(input)
                    return result
            else:
                return []

Parameter Information
---------------------
The "ParameterType" table stores the parameter types used in the system. These parameter types are divided into three types: user type, department and city.

.. code-block:: python

    query = """DROP TABLE IF EXISTS ParameterType CASCADE """
    cursor.execute(query)
    query = """CREATE TABLE ParameterType (
                      ID SERIAL PRIMARY KEY,
                      Name VARCHAR(100))"""
    cursor.execute


"ParameterInfo" keeps information such as user type, department and city used in the system. "ParameterInfo" table is connected to the "ParameterType" table with foreign key. This table contains the parameters that other tables should use. The parameter table is referenced in many tables with the foreign key.

.. code-block:: python

    query = """DROP TABLE IF EXISTS ParameterInfo CASCADE """
    cursor.execute(query)
    query = """CREATE TABLE ParameterInfo (
                      ID SERIAL PRIMARY KEY,
                      TypeID INT NOT NULL,
                      Name VARCHAR(100) NOT NULL,
                      FOREIGN KEY (TypeID) REFERENCES ParameterType(ID) ON DELETE RESTRICT)"""
    cursor.execute(query)

Parameter Add
^^^^^^^^^^^^^

Adding parameter to "ParameterInfo" table.

.. code-block:: python

    def add_parameter(cls, name, typeID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO ParameterInfo(TypeID, Name) VALUES (%s, %s)"""
            try:
                cursor.execute(query, (str(typeID), str(name)))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

Duty Operations
---------------

Duty Information
^^^^^^^^^^^^^^^^

Duty reports of doctors are kept in "DutyInfo" table. DoctorID has been used as an foreign key to find the doctor who created the user in "PersonalInfo" table. In addition, Patient count, report, shiftDate, createDate, and updateDate of duty kept in this table.

.. code-block:: python

    query = """DROP TABLE IF EXISTS DutyInfo CASCADE """
    cursor.execute(query)
    query = """CREATE TABLE DutyInfo (
                      DutyID SERIAL PRIMARY KEY,
                      DoctorID INT NOT NULL,
                      PatientCount INT DEFAULT 0,
                      Report VARCHAR(500),
                      ShiftDate TIMESTAMP NOT NULL,
                      CreateDate TIMESTAMP NOT NULL,
                      UpdateDate TIMESTAMP,
                      FOREIGN KEY (DoctorID) REFERENCES PersonalInfo(UserID) ON DELETE CASCADE)"""
    cursor.execute(query)


Duty List
^^^^^^^^^

select_all_duty_info is using for to take all duty reports in system. Also doctor name is taken from "PersonalInfo" table with using foreign key.

.. code-block:: python

    def select_all_duty_info(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            dutyInfo = None

            query = 'SELECT d.DutyID, d.DoctorID, p.Name, p.Surname, d.PatientCount, d.Report, d.ShiftDate, d.CreateDate' \
                    ' FROM DutyInfo d, PersonalInfo p Where d.DoctorID = p.UserID'
            try:
                cursor.execute(query, )
                dutyInfo = cursor.fetchall()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if dutyInfo:
                return dutyInfo
            else:
                return []


Duty Add
^^^^^^^^

add_duty

add_duty is using for adding duty report.

.. code-block:: python

    def add_duty(cls, doctorID, patientCount, report, shiftDate):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO DutyInfo(DoctorID, PatientCount, Report, ShiftDate, CreateDate) VALUES ('" + str(doctorID) + \
                    "', '" + str(patientCount) + "', '" + report + "', '" + shiftDate + "', '" + str(datetime.datetime.now()) + "')"
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return


Duty Update
^^^^^^^^^^^

update_duty is using for updating duty report. Only the data entered by the user is being updated.

.. code-block:: python

    def update_duty(cls, dutyID, patientCount, report, shiftDate):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = 'UPDATE DutyInfo SET UpdateDate = ' + "'" + str(datetime.datetime.now()) + "'"

            if patientCount != '' and patientCount is not None:
                query = query + ", PatientCount = '" + str(patientCount) + "'"
            if report != '' and report is not None:
                query = query + ", Report = '" + str(report) + "'"
            if shiftDate != '' and shiftDate is not None:
                query = query + ", ShiftDate = '" + str(shiftDate) + "'"
            query = query + ' WHERE DutyID = ' + str(dutyID)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return


Duty Delete
^^^^^^^^^^^

delete_duty_info function is using for deleting duty report.

.. code-block:: python

    def delete_duty_info(cls, dutyID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM DutyInfo WHERE DutyID = %s"""
            try:
                cursor.execute(query, dutyID)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            return