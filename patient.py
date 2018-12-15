from flask_login import UserMixin
from database import *


class Patient(UserMixin):
    def __init__(self, patientId, tckn, createUserID, birthPlace, gsm, eMail, name, surname, birthDay, updateDate):
        self.id = patientId
        self.CreateUserID = createUserID
        self.TCKN = tckn
        self.BirthPlace = birthPlace
        self.GSM = gsm
        self.EMail = eMail
        self.Name = name
        self.Surname = surname
        self.BirthDay = birthDay
        self.UpdateDate = updateDate
