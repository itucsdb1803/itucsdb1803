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
    def add_room(cls, departmentid, roomno, capacity, bathroomcount):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RoomInfo(DepartmentID, RoomNo, Capacity, BathroomCount, LastControl, CreateDate, UpdateDate) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, str(departmentid), str(roomno), str(capacity), str(bathroomcount), datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now())
            except dbapi2.Error:
                connection.rollback()
                return -1
            else:
                connection.commit()
            cursor.close()
            return 1

    @classmethod
    def update_room(cls, roomid, departmentid, roomno, capacity, bathroomCount):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = 'UPDATE RoomInfo SET UpdateDate = ' + "'" + str(datetime.datetime.now()) + "'"

            if departmentid != '' and departmentid is not None:
                query = query + ", DepartmentId = '" + str(departmentid) + "'"
            if roomno != '' and roomno is not None:
                query = query + ", RoomNo = '" + str(roomno) + "'"
            if capacity != '' and capacity is not None:
                query = query + ", Capacity = '" + str(capacity) + "'"
            if bathroomCount != '' and bathroomCount is not None:
                query = query + ", BathroomCount = '" + str(bathroomCount) + "'"
            query = query + ' WHERE RoomId = ' + str(roomid)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return

    @classmethod
    def delete_room_info(cls, roomId):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM RoomInfo WHERE RoomID = %s"""
            try:
                cursor.execute(query, (roomId))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            return

    @classmethod
    def select_room_info(cls, roomId):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            roomInfo = None

            query = """SELECT r.RoomID, r.DepartmentID, r.RoomNo, r.Capacity, r.BathroomCount, d.DepartmentID
                        FROM RoomInfo r, DepartmentInfo d
                        WHERE r.DepartmentID = r.DepartmentID AND RoomID = %s"""

            try:
                cursor.execute(query, str(roomId))
                roomInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if roomInfo:
                return roomInfo
            else:
                return []

    @classmethod
    def select_all_room_info(cls, DepartmentID):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            roomInfo = None

            if DepartmentID == '' or DepartmentID == None:
                query = """SELECT * FROM RoomInfo"""
            else:
                query = 'SELECT * FROM RoomInfo WHERE DepartmentID = ' + DepartmentID
            try:
                cursor.execute(query, )
                roomInfo = cursor.fetchall()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            if roomInfo:
                return roomInfo
            else:
                return -1