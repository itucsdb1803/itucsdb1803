from database import *
from flask_login import UserMixin

class MedicalReport(UserMixin):
    def __init__(self, patientid, doctorid, diseaseid, treatment, prescription, report, createdate, updatedate):
        self.PatientID = patientid
        self.DoctorID = doctorid
        self.DiseaseID = diseaseid
        self.Treatment = treatment
        self.Prescription = prescription
        self.Report = report
        self.CreateDate = createdate
        self.UpdateDate = updatedate
class MedicalReportDatabase:
    @classmethod
    def add_report(cls, patientid, doctorid, diseaseid, treatment, prescription, report, createdate):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO MedicalReport(PatientID, DoctorID, DiseaseID, Treatment, Prescription, Report, CreateDate) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(patientid), str(doctorid), str(diseaseid), str(treatment), str(prescription), str(report), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()