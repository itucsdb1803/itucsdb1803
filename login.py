import psycopg2 as dbapi2
from database import *
import datetime
from flask_login import UserMixin


class Login(UserMixin):
    def __init__(self, id, username, password, lastLoginDate, createDate, updateDate):
        self.id = id
        self.UserName = username
        self.Password = password
        self.LastLoginDate = lastLoginDate
        self.CreateDate = createDate
        self.UpdateDate = updateDate


class LoginDatabase:
    @classmethod
    def add_login(cls, username, password):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO LogInfo(UserName, Password, CreateDate) VALUES (%s, %s, %s)"""
            try:
                cursor.execute(query, (str(username), str(password), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

    @classmethod
    def update_login(self, userID, username, password):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            if (username != '' and username is not None) and (password != '' and password is not None):
                query = """UPDATE LogInfo SET Username = '%s', Password = '%s', UpdateDate = '%s' WHERE UserID = %d""" \
                        % (str(username), str(password), datetime.datetime.now(), userID)
            elif username != '' and username is not None:
                query = """UPDATE LogInfo SET Username = '%s', UpdateDate = '%s' WHERE UserID = %d""" \
                        % (str(username), datetime.datetime.now(), userID)
            elif password != '' and password is not None:
                query = """UPDATE LogInfo SET Password = '%s', UpdateDate = '%s' WHERE UserID = %d""" \
                        % (str(password), datetime.datetime.now(), userID)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

    @classmethod
    def log_in_job(self, username, password):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

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
                return Login(id=logData[0], username=logData[1], password=logData[2], lastLoginDate=logData[3],
                         createDate=logData[4], updateDate=logData[5])
            else:
                return -1

    @classmethod
    def update_last_login(self, userID):
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
    def select_login_info(self, userID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM LogInfo WHERE UserID = %s"""
            try:
                cursor.execute(query, (userID))
                logInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if logInfo:
                return Login(id=logInfo[0], username=logInfo[1], password=logInfo[2], lastLoginDate=logInfo[3],
                             createDate=logInfo[4], updateDate=logInfo[5])
            else:
                return -1
