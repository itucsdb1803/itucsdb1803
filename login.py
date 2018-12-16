import psycopg2 as dbapi2
from database import *
import datetime
from flask_login import UserMixin


class Login(UserMixin):
    def __init__(self, id, username, password, isEmployee, lastLoginDate, createDate, updateDate):
        self.id = id
        self.UserName = username
        self.Password = password
        self.IsEmployee = isEmployee
        self.LastLoginDate = lastLoginDate
        self.CreateDate = createDate
        self.UpdateDate = updateDate


class LoginDatabase:
    @classmethod
    def add_login(cls, username, password, isEmployee):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO LogInfo(UserName, Password, isEmployee, CreateDate) VALUES (%s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(username), str(password), str(isEmployee), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()

    @classmethod
    def change_password(cls, userID, password):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            if password != '' and password is not None:
                query = """UPDATE LogInfo SET Password = '%s', UpdateDate = '%s' WHERE UserID = %s""" \
                        % (str(password), datetime.datetime.now(), str(userID))
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

    @classmethod
    def log_in_job(cls, username, password):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            logData = None

            query = """SELECT * FROM LogInfo WHERE Username = %s AND Password = %s"""
            try:
                cursor.execute(query, (str(username), str(password)))
                logData = cursor.fetchone()

                if logData:
                    LoginDatabase.update_last_login(logData[0])

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            if logData:
                return Login(id=logData[0], username=logData[1], password=logData[2], isEmployee=logData[3],
                         lastLoginDate=logData[4], createDate=logData[5], updateDate=logData[6])
            else:
                return -1

    @classmethod
    def update_last_login(cls, userID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """UPDATE LogInfo SET LastLoginDate = %s WHERE UserID = %d""" % (datetime.datetime.now(), int(userID))
            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
        return

    @classmethod
    def select_login_info(cls, userID, username, password):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            logInfo = None

            if userID != None and userID != '':
                query = 'SELECT * FROM LogInfo WHERE UserID = ' + str(userID)
            else:
                query = "SELECT * FROM LogInfo WHERE username =  '" + username + "' AND password = '" + password + "'"
            try:
                cursor.execute(query)
                logInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if logInfo:
                return Login(id=logInfo[0], username=logInfo[1], password=logInfo[2], isEmployee=logInfo[3],
                         lastLoginDate=logInfo[4], createDate=logInfo[5], updateDate=logInfo[6])
            else:
                return -1

    @classmethod
    def username_validator(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            logInfo = None

            query = "SELECT COUNT(*) FROM LogInfo WHERE username = %s" % (str("'" + username + "'"))
            try:
                cursor.execute(query)
                logInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if logInfo[0] == 0:
                return True
            else:
                return False

    @classmethod
    def user_search(cls, username, name, surname, isEmployee):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            logInfo = None
            query = "SELECT l.UserID, l.username, p.name, p.surname,"
            if isEmployee == "True":
                query = query + " par.name, p.TelNo FROM LogInfo l, personalInfo p, parameterInfo par WHERE l.UserID = p.UserID AND p.usertype = par.ID"
                if username is not None and username != "":
                    query = query + " AND l.username like '%" + username + "%'"
                if name is not None and name != "":
                    query = query + " AND p.name like '%" + name + "%'"
                if surname is not None and surname != "":
                    query = query + " AND p.surname like '%" + surname + "%'"
            else:
                query = query + "  p.GSM FROM LogInfo l, patientInfo p WHERE l.UserID = p.patientID"
                if username is not None and username != "":
                    query = query + " AND l.username like '%" + username + "%'"
                if name is not None and name != "":
                    query = query + " AND p.name like '%" + name + "%'"
                if surname is not None and surname != "":
                    query = query + " AND p.surname like '%" + surname + "%'"
            try:
                cursor.execute(query)
                logInfo = cursor.fetchall()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            result = []
            if logInfo:
                if isEmployee == "True":
                    for log in logInfo:
                        input = [log[0], log[1], log[2], log[3], log[4], log[5], "/personal/"]
                        result.append(input)
                    return result
                else:
                    for log in logInfo:
                        input = [log[0], log[1], log[2], log[3], log[4], "Patient", "/patient/"]
                        result.append(input)
                    return result
            else:
                return []
