from flask_login import UserMixin
from database import *


class Patient(UserMixin):
    def __init__(self, patientId, tckn, createUserID, birthPlace, gsm, name, surname, birthDay, updateDate):
        self.id = patientId
        self.CreateUserID = createUserID
        self.TCKN = tckn
        self.BirthPlace = birthPlace
        self.GSM = gsm
        self.Name = name
        self.Surname = surname
        self.BirthDay = birthDay
        self.UpdateDate = updateDate


class PatientDatabase:
    @classmethod
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

    @classmethod
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

    @classmethod
    def select_patient_info(cls, patientID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            patientInfo = None

            query = """SELECT p.PatientID, p.TCKN, p.BirthPlace, para.name, p.GSM, p.Name, p.Surname, p.BirthDay  
                FROM PatientInfo p, ParameterInfo para WHERE p.BirthPlace = para.ID AND p.PatientID = %s"""
            try:
                cursor.execute(query, str(patientID))
                patientInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if patientInfo:
                return patientInfo
            else:
                return []

    @classmethod
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
