from database import *


class Duty:
    def __init__(self, dutyID, doctorID, patientCount, report, shiftDate, createDate):
        self.DutyID = dutyID
        self.DoctorID = doctorID
        self.PatientCount = patientCount
        self.Report = report
        self.ShiftDate = shiftDate
        self.CreateDate = createDate


class DutyDatabase:
    @classmethod
    def add_personal(cls, doctorID, patientCount, report, shiftDate):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = 'INSERT INTO DutyInfo(DoctorID, PatientCount, Report, ShiftDate, CreateDate) VALUES (%s, %s, %s, %s, %s)'
            try:
                cursor.execute(query, (str(doctorID), str(patientCount), str(report), str(shiftDate), datetime.datetime.now))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

    @classmethod
    def select_duty_info(cls, dutyID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            dutyInfo = None

            query = """SELECT * FROM DutyInfo WHERE DutyID = %s"""
            try:
                cursor.execute(query, (dutyID))
                dutyInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if dutyInfo:
                return Duty(DutyID=dutyInfo[0], DoctorID=dutyInfo[1], PatientCount=dutyInfo[2],
                            Report=dutyInfo[3], ShiftDate=dutyInfo[4], CreateDate=dutyInfo[5])
            else:
                return -1

    @classmethod
    def select_all_duty_info(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            dutyInfo = None

            query = 'SELECT * FROM DutyInfo'
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
                return -1
