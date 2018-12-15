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
    def add_personal(cls, UserID, hospitalID, departmentID, createUserID, userType, regNu, birthPlace, name, surname, birthDay):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO PersonalInfo(UserID, HospitalID, DepartmentID, createUserID, UserType, RegNu, BirthPlace, Name, Surname, BirthDay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(UserID), str(hospitalID), str(departmentID), str(createUserID), str(userType), str(regNu), str(birthPlace), str(name), str(surname), str(birthDay)))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

    @classmethod
    def update_personal(cls, userID, hospitalID, departmentID, userType, regNu, birthPlace, name, surname, birthDay):
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

    @classmethod
    def select_personal_info(cls, userID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            personalInfo = None

            query = """SELECT * FROM PersonalInfo WHERE UserID = %s"""
            try:
                cursor.execute(query, (userID))
                personalInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if personalInfo:
                return Personal(id=personalInfo[0], HospitalID=personalInfo[1], DepartmentID=personalInfo[2],
                                CreateUserID=personalInfo[3],
                                UserType=personalInfo[4], RegNu=personalInfo[5], BirthPlace=personalInfo[6],
                                Surname=personalInfo[7], BirthDay=personalInfo[8], UpdateDate=personalInfo[9])
            else:
                return -1

    @classmethod
    def select_all_personal_info(cls, UserType):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            personalInfo = None

            if UserType == '' or UserType == None:
                query = """SELECT * FROM PersonalInfo"""
            else:
                query = 'SELECT * FROM PersonalInfo WHERE UserType = ' + UserType
            try:
                cursor.execute(query,)
                personalInfo = cursor.fetchall()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if personalInfo:
                return personalInfo
            else:
                return -1

    @classmethod
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