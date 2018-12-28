Parts Done By Bilal Can
=======================

Bilal Can is responsible for the tables DiseaseInfo, MedicalReport, and Reservation. Tables are created inside database.py.

DiseaseInfo Table & Methods
----------------------------

This table is for adding diseases into the database.

:1) Creation of the table DiseaseInfo:

.. code-block:: python

	query = """DROP TABLE IF EXISTS DiseaseInfo CASCADE"""
    cursor.execute(query)
    query = """CREATE TABLE DiseaseInfo(
                                            DiseaseID SERIAL PRIMARY KEY,
                                            Department INT NOT NULL,
                                            Name VARCHAR(150) NOT NULL,
                                            DiseaseArea VARCHAR(150),
                                            Description VARCHAR(500),
                                            CreateDate TIMESTAMP NOT NULL,
                                            UpdateDate TIMESTAMP,
                                            FOREIGN KEY (Department) REFERENCES DepartmentInfo(DepartmentID)
                                        )"""
    cursor.execute(query)
	
:2) Adding diseases into the database:

This operation is done under /disease page. Disease.py file includes the code about adding. Pages.py give oppurtunity of communication between the html document and the Disease.py file.

.. code-block:: python

	class DiseaseDatabase:
    @classmethod
    def add_disease(cls, department, name, diseasearea, description):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO DiseaseInfo(Department, Name, DiseaseArea, Description, CreateDate) VALUES (%s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(department), str(name), str(diseasearea), str(description), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
                return -1
            else:
                connection.commit()
            cursor.close()
            return 1
			
:3) Selection of diseases:

.. code-block:: python

	@classmethod
    def select_disease(self, diseaseid):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM DiseaseInfo WHERE DiseaseID = %s"""
            try:
                cursor.execute(query, (diseaseid))
                sicknessInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            if sicknessInfo:
                return Disease(diseaseid=sicknessInfo[0], department=sicknessInfo[1], name=sicknessInfo[2],
                               diseasearea=sicknessInfo[3],
                               description=sicknessInfo[4], createdate=sicknessInfo[5], updatedate=sicknessInfo[6])
            else:
                return -1
				
MedicalReport Table & Methods
----------------------------

This is just for adding reports, in each time a new report should be added via doctors. Patients cannat see report adding page, butthey can see their medical reports.

:1) Creation of the table MedicalReport:

İt is created under database.py and coded like below.

.. code-block:: python

	query = """DROP TABLE IF EXISTS MedicalReport CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE MedicalReport(
                                            PatientID INT PRIMARY KEY,
                                            DoctorID INT NOT NULL,
                                            DiseaseID INT NOT NULL,
                                            Treatment VARCHAR(500),
                                            Prescription VARCHAR(500),
                                            Report VARCHAR(1000),
                                            CreateDate TIMESTAMP NOT NULL,
                                            UpdateDate TIMESTAMP,
                                            FOREIGN KEY (PatientID) REFERENCES PatientInfo(PatientID),
                                            FOREIGN KEY (DoctorID) REFERENCES PersonalInfo(UserID),
                                            FOREIGN KEY (DiseaseID) REFERENCES DiseaseInfo(DiseaseID)
                                                    )"""
            cursor.execute(query)
			
:2) Adding a MedicalReport:

For adding a medicalreport medicalreport.py is used. Codes are like below. Only Personnels of a hospital can access here.

.. code-block:: python

	from database import *
	class MedicalReport():
    def __init__(self, patientid, doctorid, diseaseid, treatment, prescription, report, createdate, updatedate):
        self.PatientID = patientid
        self.DoctorID = doctorid
        self.DiseaseID = diseaseid
        self.Treatment = treatment
        self.Prescription = prescription
        self.Report = report
        self.CreateDate = createdate
        self.UpdateDate = updatedate
	class MedicalReportDatabase:
    @classmethod
    def add_report(cls, patientid, doctorid, diseaseid, treatment, prescription, report):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO MedicalReport(PatientID, DoctorID, DiseaseID, Treatment, Prescription, Report, CreateDate) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(patientid), str(doctorid), str(diseaseid), str(treatment), str(prescription), str(report), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
                return -1
            else:
                connection.commit()
            cursor.close()
            return 1
			
Reservation Table & Methods
----------------------------

Users can do reservations; also, the personnel of the hospital can make reservations for patients. Patients can see their information about reservations, and they can change the reservations information later.

:1) Creating Table for Reservations:

It is created under databse.py with the code below.

.. code-block:: python

	query = """DROP TABLE IF EXISTS Reservation CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE Reservation (
                                                ReservationID SERIAL PRIMARY KEY,
                                                PatientID INT NOT NULL,
                                                HospitalID INT NOT NULL,
                                                DoctorID INT NOT NULL,
                                                DepartmentID INT NOT NULL,
                                                DiseaseID INT NOT NULL,
                                                Comment VARCHAR(500),
                                                UpdateDate TIMESTAMP,
                                                CreateDate TIMESTAMP NOT NULL,
                                                ReservationDate TIMESTAMP NOT NULL,
                                                ReservationHour VARCHAR(10),
                                                FOREIGN KEY (PatientID) REFERENCES PatientInfo(PatientID),
                                                FOREIGN KEY (HospitalID) REFERENCES HospitalInfo(HospitalID),
                                                FOREIGN KEY (DoctorID) REFERENCES PersonalInfo(UserID),
                                                FOREIGN KEY (DepartmentID) REFERENCES DepartmentInfo(DepartmentID),
                                                FOREIGN KEY (DiseaseID) REFERENCES DiseaseInfo(DiseaseID)
                                                                )"""
            cursor.execute(query)

:2) Making a Reservation:

Under reservation file a class is formed, and it has a method for making a reservation.

.. code-block:: python

	from database import *
	from flask_login import UserMixin
	class MedicalReport(UserMixin):
    def __init__(self, reservationid, patientid, hospitalid, doctorid, departmentid, diseaseid, comment, updatedate, createdate, reservationdate, reservationhour):
        self.ReservationID = reservationid
        self.PatientID = patientid
        self.HospitalID = hospitalid
        self.DoctorID = doctorid
        self.DepartmentID = departmentid
        self.DiseaeID = diseaseid
        self.Comment = comment
        self.UpdateDate = updatedate
        self.CreateDate = createdate
        self.ReservationDate = reservationdate
        self.ReservationHour = reservationhour
	class ReservationDatabase:
    @classmethod
    def add_reservation(cls, patientid, hospitalid, doctorid, departmentid, diseaseid, comment, reservationdate, reservationhour):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO Reservation(PatientID, HospitalID, DoctorID, DepartmentID, DiseaseID, Comment, CreateDate, ReservationDate, ReservationHour) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(patientid), str(hospitalid), str(doctorid), str(departmentid), str(diseaseid), str(comment), datetime.datetime.now(), str(reservationdate), str(reservationhour)))
            except dbapi2.Error:
                connection.rollback()
                return -1
            else:
                connection.commit()
            cursor.close()
            return 1

:3) Selecting a Reservation:

The selection of reservation should be done to show them to the patients in the profile page of them. Allso after clicking "Update Reservation" button, to change the correct reservation info, we should at first get the reservationid from the database.

.. code-block:: python

	@classmethod
    def select_all_reservation_info(cls, patientid):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            reservationInfo = None
            if patientid == '' or patientid == None:
                query = """SELECT * FROM Reservation"""
            else:
                query = 'SELECT * FROM ReservationInfo WHERE PatientID = ' + patientid
            try:
                cursor.execute(query,)
                reservationInfo = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            if reservationInfo:
                return reservationInfo
            else:
                return -1
    @classmethod
    def select_reservation_info(cls, patientid):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            reservationInfo = None
            query = """SELECT  res.PatientID, res.ReservationID, res.DoctorID, res.HospitalID, res.DepartmentID, 
                            res.DiseaseID, res.Comment, res.ReservationDate, res.ReservationHour 
                FROM  PatientInfo p, Reservation res
                    WHERE p.PatientID = res.PatientID AND p.PatientID = %s"""
            try:
                cursor.execute(query, str(patientid))
                reservationInfo = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            if reservationInfo:
                reservationInfo2 = [reservationInfo[0], reservationInfo[1], reservationInfo[2], reservationInfo[3], reservationInfo[4],
                                    reservationInfo[5], reservationInfo[6], reservationInfo[7], reservationInfo[8]]
                return reservationInfo2
            else:
                return []
				
:4) Updating a Reservation:

.. code-block:: python

	@classmethod
    def update_reservation(cls, reservationid, patientid, hospitalid, doctorid, departmentid, diseaseid, comment, reservationdate, reservationhour):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = 'UPDATE Reservation SET UpdateDate = ' + "'" + str(datetime.datetime.now()) + "'"

            if patientid != '' and patientid is not None:
                query = query + ", PatientID = '" + str(patientid) + "'"
            if hospitalid != '' and hospitalid is not None:
                query = query + ", HospitalID = '" + str(hospitalid) + "'"
            if doctorid != '' and doctorid is not None:
                query = query + ", DoctorID = '" + str(doctorid) + "'"
            if departmentid != '' and departmentid is not None:
                query = query + ", DepartmentID = '" + str(departmentid) + "'"
            if diseaseid != '' and diseaseid is not None:
                query = query + ", DiseaseID = '" + str(diseaseid) + "'"
            if comment != '' and comment is not None:
                query = query + ", Comment = '" + str(comment) + "'"
            if reservationdate != '' and reservationdate is not None:
                query = query + ", ReservationDate = '" + str(reservationdate) + "'"
            if reservationhour != '' and reservationhour is not None:
                query = query + ", ReservationHour = '" + str(reservationhour) + "'"
            query = query + ' WHERE ReservationId = ' + str(reservationid)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return