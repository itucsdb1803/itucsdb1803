from database import *

class Parameter():
    def __init__(self, id, typeID, name):
        self.ID = id
        self.TypeID = typeID
        self.Name = name

class ParameterDatabase:
    @classmethod
    def select_parameters_with_type(cls, typeID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM ParameterInfo WHERE TypeID = %s"""

            try:
                cursor.execute(query, str(typeID))
                parameterInfo = cursor.fetchall()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if parameterInfo:
                return parameterInfo
            else:
                return [[]]