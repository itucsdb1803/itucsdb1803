Parts Done By Bilal Can
=======================

Bilal Can is responsible for the tables DiseaseInfo, MedicalReport, and Reservation. Tables are created inside database.py.

DiseaseInfo Table & Methods
----------------------------

This table is for adding diseases into the database.

:1)Creation of the table DiseaseInfo

.. code-block:: python
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
	
:2)Adding diseases into the database

This operation is done under /disease page. Disease.py file includes the code about adding. Pages.py give oppurtunity of communication between the html document and the Disease.py file.

.. code-block:: python
	class DiseaseDatabase:
    @classmethod
    def add_disease(cls, department, name, diseasearea, description):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO DiseaseInfo(Department, Name, DiseaseArea, Description, CreateDate) VALUES (%s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(department), str(name), str(diseasearea), str(description), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
                return -1
            else:
                connection.commit()
            cursor.close()
            return 1
			
:3)Selection of diseases

.. code-block:: python
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