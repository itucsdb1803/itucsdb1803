import os
import psycopg2 as dbapi2
import datetime
import init_parameters


city_dict = init_parameters.city_dict
job_dict = init_parameters.job_dict
dep_dict = init_parameters.department_dict


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

            query = """DROP TABLE IF EXISTS ParameterType CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE ParameterType (
                                                            ID SERIAL PRIMARY KEY,
                                                            Name VARCHAR(100)
                                                                            )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS ParameterInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE ParameterInfo (
                                                            ID SERIAL PRIMARY KEY,
                                                            TypeID INT NOT NULL,
                                                            Name VARCHAR(100) NOT NULL,
                                                            FOREIGN KEY (TypeID) REFERENCES ParameterType(ID)
                                                                            )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS LogInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE LogInfo (
                                                UserID SERIAL PRIMARY KEY,
                                                UserName VARCHAR(100) NOT NULL,
                                                Password VARCHAR(100) NOT NULL,
                                                IsEmployee Boolean NOT NULL,
                                                LastLoginDate TIMESTAMP,
                                                CreateDate TIMESTAMP NOT NULL,
                                                UpdateDate TIMESTAMP
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
                                                            TelNo VARCHAR(50) NOT NULL,
                                                            Name VARCHAR(100) NOT NULL,
                                                            Surname VARCHAR(100) NOT NULL,
                                                            BirthDay TIMESTAMP,
                                                            UpdateDate TIMESTAMP,
                                                            FOREIGN KEY (UserID) REFERENCES LogInfo(UserID),
                                                            FOREIGN KEY (CreateUserID) REFERENCES LogInfo(UserID),
                                                            FOREIGN KEY (BirthPlace) REFERENCES ParameterInfo(ID),
                                                            FOREIGN KEY (HospitalID) REFERENCES HospitalInfo(HospitalID),
                                                            FOREIGN KEY (DepartmentID) REFERENCES ParameterInfo(ID),
                                                            FOREIGN KEY (UserType) REFERENCES ParameterInfo(ID)
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
                                                CreateDate TIMESTAMP NOT NULL,
                                                UpdateDate TIMESTAMP,
                                                FOREIGN KEY (DoctorID) REFERENCES PersonalInfo(UserID)
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
                                                            CreateDate TIMESTAMP NOT NULL,
                                                            FOREIGN KEY (City) REFERENCES ParameterInfo(ID)
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
                                                            CreateDate TIMESTAMP NOT NULL,
                                                            FOREIGN KEY (HospitalID) REFERENCES HospitalInfo(HospitalID),
                                                            FOREIGN KEY (DepartmentTypeID) REFERENCES ParameterInfo(ID)
                                                                            )"""
            cursor.execute(query)

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
                                                UpdateDate TIMESTAMP,
                                                FOREIGN KEY (DepartmentID) REFERENCES DepartmentInfo(DepartmentID)
                                                                )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS DiseaseInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE DiseaseInfo(
                                                        DiseaseID SERIAL PRIMARY KEY,
                                                        Department INT NOT NULL,
                                                        Name VARCHAR(150) NOT NULL,
                                                        DiseaseArea VARCHAR(150),
                                                        Description VARCHAR(500),
                                                        CreateDate TIMESTAMP NOT NULL,
                                                        UpdateDate TIMESTAMP,
                                                        FOREIGN KEY (Department) REFERENCES DepartmentInfo(DepartmentID)
                                                                )"""
            cursor.execute(query)

            query = """DROP TABLE  IF EXISTS PatientInfo CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE PatientInfo(
                                                         PatientID INT PRIMARY KEY,
                                                         CreateUserID INT NOT NULL,
                                                         BirthPlace INT NOT NULL,
                                                         GSM VARCHAR(50) NOT NULL,
                                                         TCKN VARCHAR(50) NOT NULL,
                                                         Name VARCHAR(100) NOT NULL,
                                                         Surname VARCHAR(100) NOT NULL,
                                                         BirthDay TIMESTAMP NOT NULL,
                                                         UpdateDate TIMESTAMP,
                                                         FOREIGN KEY (PatientID) REFERENCES LogInfo(UserID),
                                                         FOREIGN KEY (CreateUserID) REFERENCES LogInfo(UserID),
                                                         FOREIGN KEY (BirthPlace) REFERENCES ParameterInfo(ID)
                                                                )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS Reservation CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE Reservation (
                                                ReservationID SERIAL PRIMARY KEY,
                                                PatientID INT NOT NULL,
                                                HospitalID INT NOT NULL,
                                                DoctorID INT NOT NULL,
                                                DepartmentID INT NOT NULL,
                                                DiseaseID INT NOT NULL,
                                                Comment VARCHAR(500),
                                                UpdateDate TIMESTAMP,
                                                CreateDate TIMESTAMP NOT NULL,
                                                ReservationDate TIMESTAMP NOT NULL,
                                                FOREIGN KEY (PatientID) REFERENCES PatientInfo(PatientID),
                                                FOREIGN KEY (HospitalID) REFERENCES HospitalInfo(HospitalID),
                                                FOREIGN KEY (DoctorID) REFERENCES PersonalInfo(UserID),
                                                FOREIGN KEY (DepartmentID) REFERENCES DepartmentInfo(DepartmentID),
                                                FOREIGN KEY (DiseaseID) REFERENCES DiseaseInfo(DiseaseID)
                                                                )"""
            cursor.execute(query)

            query = """DROP TABLE IF EXISTS MedicalReport CASCADE"""
            cursor.execute(query)
            query = """CREATE TABLE MedicalReport(
                                            PatientID INT PRIMARY KEY,
                                            DoctorID INT NOT NULL,
                                            DiseaseID INT NOT NULL,
                                            Treatment VARCHAR(500),
                                            Prescription VARCHAR(500),
                                            Report VARCHAR(1000),
                                            CreateDate TIMESTAMP NOT NULL,
                                            UpdateDate TIMESTAMP,
                                            FOREIGN KEY (PatientID) REFERENCES PatientInfo(PatientID),
                                            FOREIGN KEY (DoctorID) REFERENCES PersonalInfo(UserID),
                                            FOREIGN KEY (DiseaseID) REFERENCES DiseaseInfo(DiseaseID)
                                                    )"""
            cursor.execute(query)


    def init_db(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO LogInfo(UserName, Password, IsEmployee, CreateDate) VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, ("admin", "12345", "true", datetime.datetime.now()))

            query = """INSERT INTO ParameterType(ID, Name) VALUES (%s, %s)"""
            cursor.execute(query, ("1", "City"))

            query = """INSERT INTO ParameterType(ID, Name) VALUES (%s, %s)"""
            cursor.execute(query, ("2", "Duty"))

            query = """INSERT INTO ParameterType(ID, Name) VALUES (%s, %s)"""
            cursor.execute(query, ("3", "Department Type"))

            query = """INSERT INTO ParameterInfo(TypeID, Name) VALUES (1, %(city)s)"""
            cursor.executemany(query, city_dict)

            query = """INSERT INTO ParameterInfo(TypeID, Name) VALUES (2, %(job)s)"""
            cursor.executemany(query, job_dict)

            query = """INSERT INTO ParameterInfo(TypeID, Name) VALUES (3, %(dep)s)"""
            cursor.executemany(query, dep_dict)

database = DatabaseOperations()