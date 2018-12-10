from flask_login import UserMixin
from database import *

class Personal(UserMixin):
    def __init__(self, id, hospitalid, departmentID, createUserID, userType, regNu, birthPlace, name, surname, birthDay, updateDate):
        self.id = id
        self.HospitalID = hospitalid
        self.DepartmentID = departmentID
        self.CreateUserID = createUserID
        self.UserType = userType
        self.RegNu = regNu
        self.BirthPlace = birthPlace
        self.Name = name
        self.Surname = surname
        self.BirthDay = birthDay
        self.UpdateDate = updateDate

class PersonalDatabase:
    @classmethod
    def add_personal(cls, UserID, hospitalid, departmentID, createUserID, userType, regNu, birthPlace, name, surname, birthDay):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PersonalInfo(UserID, HospitalID, DepartmentID, createUserID, UserType, RegNu, BirthPlace, Name, Surname, BirthDay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(UserID), str(hospitalid), str(departmentID), str(createUserID), str(userType), str(regNu), str(birthPlace), str(name), surname, None))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()