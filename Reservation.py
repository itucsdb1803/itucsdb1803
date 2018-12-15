from database import *
from flask_login import UserMixin

class MedicalReport(UserMixin):
    def __init__(self, reservationid, patientid, hospitalid, doctorid, departmentid, updatedate, createdate, reservationdate):
        self.ReservationID = reservationid
        self.PatientID = patientid
        self.HospitalID = hospitalid
        self.DoctorID = doctorid
        self.DepartmentID = departmentid
        self.UpdateDate = updatedate
        self.CreateDate = createdate
        self.ReservationDate = reservationdate

class MedicalReportDatabase:
    @classmethod
    def add_report(cls, patientid, hospitalid, doctorid, departmentid, reservationdate):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO MedicalReport(PatientID, HospitalID, DoctorID, DepartmentID, CreateDate, ReservationDate) VALUES (%s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(patientid), str(hospitalid), str(doctorid), str(departmentid), datetime.datetime.now(), str(reservationdate)))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            