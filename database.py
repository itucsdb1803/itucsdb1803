import os
import psycopg2 as dbapi2

class DatabaseOperations:
    def __init__(self):

        DATABASE_URL = os.getenv('DATABASE_URL')

        if DATABASE_URL is not None:
            self.config = DATABASE_URL
        else:
            self.config = """user='postgres' password='12345' host='localhost' port=5432 dbname='itucsdb1803'"""

    # @classmethod
        #    def get_elephantsql_dsn(cls, vcap_services):
        #"""Returns the data source name for ElephantSQL."""
        #parsed = json.loads(vcap_services)
        #uri = parsed["elephantsql"][0]["credentials"]["uri"]
        #match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
        #user, password, host, _, port, dbname = match.groups()
            #dsn = """user='{}' password='{}' host='{}' port={}
        #    dbname='{}'""".format(user, password, host, port, dbname)
    #return dsn"""

    def create_tables(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            """ UTKU's TABLE START """
            query = """DROP TABLE IF EXISTS LogInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE LogInfo (
                                                 ID SERIAL PRIMARY KEY,
                                                 UserName VARCHAR(100) NOT NULL,
                                                 Password VARCHAR(100) NOT NULL,
                                                 LastLoginDate TIMESTAMP,
                                                 CreateDate TIMESTAMP NOT NULL,
                                                 UpdateDate TIMESTAMP
                                                                )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS DutyInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE DutyInfo (
                                                             DutyID SERIAL PRIMARY KEY,
                                                             DoctorID INT NOT NULL,
                                                             PatientCount INT DEFAULT 0,
                                                             Report VARCHAR(500),
                                                             ShiftDate TIMESTAMP NOT NULL,
                                                             CreateDate TIMESTAMP NOT NULL
                                                                            )"""
            cursor.execute(query)
            """ UTKU's TABLE END """

            """ ORHAN's TABLE START """

            query = """DROP TABLE IF EXISTS RoomInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE RoomInfo (
                                                RoomID SERIAL PRIMARY KEY,
                                                DepartmentID INT,
                                                RoomNo INT NOT NULL,
                                                Capacity INT NOT NULL,
                                                BathroomCount INT,
                                                LastControl TIMESTAMP,
                                                CreateDate TIMESTAMP NOT NULL,
                                                UpdateDate TIMESTAMP
                                                                )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS DepartmentInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE DepartmentInfo (
                                                DepartmentID SERIAL PRIMARY KEY,
                                                HospitalID INT,
                                                DepartmentTypeID INT,
                                                RoomCount INT,
                                                BlockNumber INT,
                                                PersonalCount INT,
                                                CreateDate TIMESTAMP NOT NULL
                                                                )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS HospitalInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE HospitalInfo (
                                                HospitalID SERIAL PRIMARY KEY,
                                                City INT NOT NULL,
                                                Capacity INT NOT NULL,
                                                Address VARCHAR(500) NOT NULL,
                                                Name VARCHAR(250) NOT NULL,
                                                CreateDate TIMESTAMP NOT NULL
                                                                )"""
            cursor.execute(query)

            """ ORHAN's TABLE END """

            """BILAL's TABLES START"""
            query = """DROP TABLE  IF EXISTS PatientInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE PatientInfo(
                                             PatientID SERIAL PRIMARY KEY,
                                             UserID INTEGER NOT NULL,
                                             DiseaseID INTEGER NOT NULL,
                                             CreateUserID INTEGER NOT NULL,
                                             TCKN INTEGER NOT NULL,
                                             BirthPlace INTEGER NOT NULL,
                                             Name VARCHAR(100) NOT NULL,
                                             Surname VARCHAR(100) NOT NULL,
                                             BirthDay TIMESTAMP NOT NULL,
                                             CreateDate TIMESTAMP NOT NULL
                                                    )"""
            cursor.execute(query)
            """BILAL's TABLES START"""