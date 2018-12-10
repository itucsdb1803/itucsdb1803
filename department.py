from database import *

class Department():
    def __init__(self, departmentid, hospitalid, deptypeid, roomcount, blocknumber, personalcount, createDate):
        self.DepartmentID = departmentid
        self.HospitalID = hospitalid
        self.DepartmentTypeID = deptypeid
        self.RoomCount = roomcount
        self.BlockNumber = blocknumber
        self.PersonalCount = personalcount
        self.CreateDate = createDate

class DepartmentDatabase:
    @classmethod
    def add_department(cls, departmentid, hospitalid, deptypeid, roomcount, blocknumber, personalcount):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO DepartmentInfo(DepartmentID, HospitalID, DepartmentTypeID, RoomCount, BlockNumber, PersonalCount, CreateDate) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(departmentid), str(hospitalid), str(deptypeid), str(roomcount), str(blocknumber), str(personalcount), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()