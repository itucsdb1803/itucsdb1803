from flask_login import UserMixin
from database import *

class Personal(UserMixin):
    def __init__(self, id, hospitalid, departmentID, createUserID, userType, regNu, telNo, birthPlace, name, surname, birthDay, updateDate):
        self.id = id
        self.HospitalID = hospitalid
        self.DepartmentID = departmentID
        self.CreateUserID = createUserID
        self.UserType = userType
        self.RegNu = regNu
        self.TelNo = telNo
        self.BirthPlace = birthPlace
        self.Name = name
        self.Surname = surname
        self.BirthDay = birthDay
        self.UpdateDate = updateDate

class PersonalDatabase:
    @classmethod
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

    @classmethod
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

    @classmethod
    def select_personal_info(cls, userID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            personalInfo = None

            query = """SELECT p.UserID, p.HospitalID, h.name, p.DepartmentID, para1.name, p.UserType, para2.Name, p.RegNu, p.TelNo, p.BirthPlace, para3.Name, p.Name, p.Surname, p.BirthDay
                FROM PersonalInfo p, ParameterInfo para1, ParameterInfo para2, ParameterInfo para3, HospitalInfo h 
                    WHERE p.DepartmentID = para1.ID AND p.UserType = para2.ID AND p.BirthPlace = para3.ID AND p.HospitalID = h.HospitalID
                        AND UserID = %s"""
            try:
                cursor.execute(query, str(userID))
                personalInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if personalInfo:
                return personalInfo
            else:
                return []

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


    @classmethod
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
