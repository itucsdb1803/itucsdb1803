from database import *
from flask_login import UserMixin

class MedicalReport(UserMixin):
    def __init__(self, reservationid, patientid, hospitalid, doctorid, departmentid, diseaseid, comment, updatedate, createdate, reservationdate):
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

class ReservationDatabase:
    @classmethod
    def add_reservation(cls, patientid, hospitalid, doctorid, departmentid, diseaseid, comment, reservationdate, reservationhour):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO Reservation(PatientID, HospitalID, DoctorID, DepartmentID, DiseaseID, Comment, CreateDate, ReservationDate, ReservationHour) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(patientid), str(hospitalid), str(doctorid), str(departmentid), str(diseaseid),str(comment), datetime.datetime.now(), str(reservationdate), str(reservationhour)))
            except dbapi2.Error:
                connection.rollback()
                return -1
            else:
                connection.commit()
            cursor.close()
            return 1
