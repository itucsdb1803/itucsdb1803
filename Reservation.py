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