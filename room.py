from database import *

class Room():
    def __init__(self, roomid, departmentid, roomno, capacity, bathroomcount, lastcontrol, createDate, updatedate):
        self.RoomID = roomid
        self.DepartmentID = departmentid
        self.RoomNo = roomno
        self.Capacity = capacity
        self.BathroomCount = bathroomcount
        self.LastControl = lastcontrol
        self.CreateDate = createDate
        self.UpdateDate = updatedate

class RoomDatabase:
    @classmethod
    def add_room(cls, roomid, departmentid, roomno, capacity, bathroomcount):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RoomInfo(RoomID, DepartmentID, RoomNo, Capacity, BathroomCount, LastControl, CreateDate, UpdateDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(roomid), str(departmentid), str(roomno), str(capacity), str(bathroomcount), datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()