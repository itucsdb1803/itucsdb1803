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
    def add_disease(cls, department, name, diseasearea, description,):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            print(department)
            query = """INSERT INTO DiseaseInfo(Department, Name, DiseaseArea, Description, CreateDate) VALUES (%s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(department), str(name), str(diseasearea), str(description), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()


    @classmethod
    def select_disease(self, diseaseid):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM DiseaseInfo WHERE DiseaseID = %s"""
            try:
                cursor.execute(query, (diseaseid))
                sicknessInfo = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            if sicknessInfo:
                return Disease(diseaseid=sicknessInfo[0], department=sicknessInfo[1], name=sicknessInfo[2],
                               diseasearea=sicknessInfo[3],
                               description=sicknessInfo[4], createdate=sicknessInfo[5], updatedate=sicknessInfo[6])
            else:
                return -1