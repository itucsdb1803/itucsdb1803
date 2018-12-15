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