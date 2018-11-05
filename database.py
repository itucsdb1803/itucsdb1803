import os
import json
import re
import psycopg2 as dbapi2

class DatabaseOperations:
    def __init__(self):

        VCAP_SERVICES = os.getenv('VCAP_SERVICES')

        if VCAP_SERVICES is not None:
            self.config = DatabaseOperations.get_elephantsql_dsn(VCAP_SERVICES)
        else:
            self.config = """user='postgres' password='12345' host='localhost' port=5432 dbname='itucsdb1803'"""

    @classmethod
    def get_elephantsql_dsn(cls, vcap_services):
        """Returns the data source name for ElephantSQL."""
        parsed = json.loads(vcap_services)
        uri = parsed["elephantsql"][0]["credentials"]["uri"]
        match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
        user, password, host, _, port, dbname = match.groups()
        dsn = """user='{}' password='{}' host='{}' port={}
                 dbname='{}'""".format(user, password, host, port, dbname)
        return dsn

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