from database import *

class ParameterType():
    def __init__(self, id, name):
        self.ID = id
        self.Name = name

class ParameterTypeDatabase:
    @classmethod
    def select_parameter_types(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM ParameterType"""

            try:
                cursor.execute(query)
                parameterTypeList = cursor.fetchall()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if parameterTypeList:
                return parameterTypeList
            else:
                return [[]]