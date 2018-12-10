from database import *

class Disease():
    def __init__(self, diseaseid, department, name, diseasearea, description, createdate, updatedate):
        self.DiseaseID = diseaseid
        self.Department = department
        self.Name = name
        self.DiseaseArea = diseasearea
        self.Description = description
        self.CreateDate = createdate
        self.UpdateDate = updatedate

class DiseaseDatabase:
    @classmethod
    def add_disease(cls, diseaseid, department, name, diseasearea, description, createdate, updatedate):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO DiseaseInfo(DiseaseID, Department, Name, DiseaseArea, Description, CreateDate, UpdateDate) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(diseaseid), str(department), str(name), str(diseasearea), str(description), str(createdate), None))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()