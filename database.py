import os
import psycopg2 as dbapi2
import datetime

class DatabaseOperations:
    def __init__(self):

        DATABASE_URL = os.getenv('DATABASE_URL')

        if DATABASE_URL is not None:
            self.config = DATABASE_URL
        else:
            self.config = """user='postgres' password='12345' host='localhost' port=5432 dbname='itucsdb1803'"""


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

            query = """DROP TABLE IF EXISTS PersonalInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE PersonalInfo (
                                                UserID INT PRIMARY KEY,
                                                HospitalID INT NOT NULL,
                                                DepartmentID INT NOT NULL,
                                                CreateUserID INT NOT NULL,
                                                UserType INT NOT NULL,
                                                RegNu INT NOT NULL,
                                                BirthPlace INT NOT NULL,
                                                Name VARCHAR(100) NOT NULL,
                                                Surname VARCHAR(100) NOT NULL,
                                                BirthDay TIMESTAMP,
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

            query = """DROP TABLE IF EXISTS ParameterInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE ParameterInfo (
                                                ID SERIAL PRIMARY KEY,
                                                TypeID INT NOT NULL,
                                                Name VARCHAR(100) NOT NULL
                                                                )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS ParameterType CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE ParameterType (
                                                ID SERIAL PRIMARY KEY,
                                                Name VARCHAR(100)
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

            query="""DROP TABLE IF EXISTS DiseaseInfo CASCADE"""
            cursor.execute(query)
            query="""CREATE TABLE DiseaseInfo(
                                            DiseaseID SERIAL PRIMARY KEY,
                                            DepartmentID INTEGER NOT NULL,
                                            Name VARCHAR(150) NOT NULL,
                                            DiseaseArea VARCHAR(150),
                                            Description VARCHAR(500),
                                            CreateDate TIMESTAMP NOT NULL,
                                            UpdateDate TIMESTAMP
                                                    )"""
            cursor.execute(query)

            query="""DROP TABLE IF EXISTS MedicalReport CASCADE"""
            cursor.execute(query)
            query="""CREATE TABLE MedicalReport(
                                            PatientID INTEGER NOT NULL,
                                            DoctorID INTEGER NOT NULL,
                                            DiseaseID INTEGER NOT NULL,
                                            Treatment VARCHAR(500),
                                            Prescription VARCHAR(500),
                                            Report VARCHAR(1000),
                                            CreateDate TIMESTAMP NOT NULL)"""
            cursor.execute(query)
            
            """BILAL's TABLES END"""

    def init_db(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO LogInfo(UserName, Password, CreateDate) VALUES (%s, %s, %s)"""
            cursor.execute(query, ("admin", "12345", datetime.datetime.now()))
