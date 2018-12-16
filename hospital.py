from database import *

class Hospital():
    def __init__(self, hospitalid, city, capacity, address, name, createDate):
        self.HospitalID = hospitalid
        self.City = city
        self.Capacity = capacity
        self.Address = address
        self.Name = name
        self.CreateDate = createDate

class HospitalDatabase:
    @classmethod
    def add_hospital(cls, city, capacity, address, name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO HospitalInfo(City, Capacity, Address, Name, CreateDate) VALUES (%s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(city), str(capacity), str(address), str(name), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
                return -1
            else:
                connection.commit()
            cursor.close()
            return 1

    @classmethod
    def update_hospital(cls, hospitalid, city, capacity, address, name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = 'UPDATE HospitalInfo SET UpdateDate = ' + "'" + str(datetime.datetime.now()) + "'"

            if city != '' and city is not None:
                query = query + ", city = '" + str(city) + "'"
            if capacity != '' and capacity is not None:
                query = query + ", Capacity = '" + str(capacity) + "'"
            if address != '' and address is not None:
                query = query + ", address = '" + str(address) + "'"
            if name != '' and name is not None:
                query = query + ", Name = '" + str(name) + "'"
            query = query + ' WHERE HospitalId = ' + str(hospitalid)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

    @classmethod
    def delete_hospital_info(cls, hospitalId):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM HospitalInfo WHERE HospitalID = %s"""
            try:
                cursor.execute(query, (hospitalId))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            return

    @classmethod
    def select_hospital_info(cls, hospitalId):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            hospitalInfo = None

            query = """SELECT h.HospitalID, h.City, h.Capacity, h.Address, h.Name, para.ID
                        FROM HospitalInfo h, ParameterInfo para
                        WHERE h.City = para.ID AND h.HospitalID = %s"""

            try:
                cursor.execute(query, str(hospitalId))
                hospitalInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if hospitalInfo:
                return hospitalInfo
            else:
                return []

    @classmethod
    def select_all_hospital_info(cls, City):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            hospitalInfo = None

            if City == '' or City == None:
                query = """SELECT * FROM HospitalInfo"""
            else:
                query = 'SELECT * FROM HospitalInfo WHERE City = ' + City
            try:
                cursor.execute(query,)
                hospitalInfo = cursor.fetchall()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if hospitalInfo:
                return hospitalInfo
            else:
                return -1

    @classmethod
    def get_hospital_info(cls, HospitalID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            hospitalInfo = None

            query = """SELECT h.HospitalID, h.City, para.ID, para.Name, h.Capacity, h.Address, h.Name
                        FROM HospitalInfo h, ParameterInfo para
                        WHERE h.City = para.ID
                        AND h.HospitalID = %s"""

            try:
                cursor.execute(query, str(HospitalID))
                hospitalInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if hospitalInfo:
                return hospitalInfo
            else:
                return []