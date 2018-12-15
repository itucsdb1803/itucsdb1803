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

    @classmethod
    def update_department(cls, departmentid, hospitalid, departmentTypeid, roomCount, blockNumber, personalCount):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = 'UPDATE DepartmentInfo SET UpdateDate = ' + "'" + str(datetime.datetime.now()) + "'"

            if hospitalid != '' and hospitalid is not None:
                query = query + ", HospitalId = '" + str(hospitalid) + "'"
            if departmentTypeid != '' and departmentTypeid is not None:
                query = query + ", DepartmentTypeId = '" + str(departmentTypeid) + "'"
            if roomCount != '' and roomCount is not None:
                query = query + ", RoomCount = '" + str(roomCount) + "'"
            if blockNumber != '' and blockNumber is not None:
                query = query + ", BlockNumber = '" + str(blockNumber) + "'"
            if personalCount != '' and personalCount is not None:
                query = query + ", PersonalCount = '" + str(personalCount) + "'"
            query = query + 'WHERE DepartmentId = ' + str(departmentid)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

    @classmethod
    def select_department_info(cls, departmentId):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            departmentInfo = None

            query = """SELECT d.DepartmentID, d.HospitalID, d.DepartmentTypeID, d.RoomCount, d.BlockNumber, d.PersonalCount, h.HospitalID, para.TypeID
                        FROM DepartmentInfo d, HospitalInfo h, ParameterInfo para
                        WHERE d.HospitalID = h.HospitalID AND d.DepartmentTypeID = para.TypeID AND d.DepartmentID = %s"""

            try:
                cursor.execute(query, str(departmentId))
                departmentInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if departmentInfo:
                return departmentInfo
            else:
                return []