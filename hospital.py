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
    def add_hospital(cls, hospitalid, city, capacity, address, name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO HospitalInfo(HospitalID, City, Capacity, Address, Name, CreateDate) VALUES (%s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(hospitalid), str(city), str(capacity), str(address), str(name), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()

    @classmethod
    def update_hospital(cls, hospitalid, capacity, address, name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = 'UPDATE HospitalInfo SET UpdateDate = ' + "'" + str(datetime.datetime.now()) + "'"

            if capacity != '' and capacity is not None:
                query = query + ", Capacity = '" + str(capacity) + "'"
            if address != '' and address is not None:
                query = query + ", address = '" + str(address) + "'"
            if name != '' and name is not None:
                query = query + ", Name = '" + str(name) + "'"
            query = query + ' WHERE HospitalOd = ' + str(hospitalid)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

