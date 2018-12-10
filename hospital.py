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
    def add_hospital(cls, hospitalId, city, capacity, address, name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO HospitalInfo(HospitalID, City, Capacity, Address, Name, CreateDate) VALUES (%s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(hospitalId), str(city), str(capacity), str(address), str(name), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()