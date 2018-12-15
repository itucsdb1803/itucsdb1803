from flask_login import UserMixin
from database import *


class Patient(UserMixin):
    def __init__(self, patientId, tckn, createUserID, birthPlace, gsm, eMail, name, surname, birthDay, updateDate):
        self.id = patientId
        self.CreateUserID = createUserID
        self.TCKN = tckn
        self.BirthPlace = birthPlace
        self.GSM = gsm
        self.EMail = eMail
        self.Name = name
        self.Surname = surname
        self.BirthDay = birthDay
        self.UpdateDate = updateDate


class PatientDatabase:
    @classmethod
    def add_patient(cls, patientId, tckn, createUserID, birthPlace, gsm, eMail, name, surname, birthDay):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PatientInfo(PatientId, CreateUserID, TCKN, BirthPlace, GSM, EMail, Name, Surname, BirthDay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(patientId), str(createUserID), str(tckn), str(birthPlace), str(gsm), str(eMail), str(name), str(name), str(surname), str(birthDay)))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return