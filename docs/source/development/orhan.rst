Parts Done By Orhan Kurto
=========================

The main entities-tables created by me are HospitalInfo, DepartmentInfo and RoomInfo. Also a sub-table which keeps information such as city id's and department id's names as ParameterInfo. All the tables were created by using the function create_tables. The details about the tables and their methods are as follows:

HospitalInfo Table & Methods
----------------------------

HospitalInfo table is created in order to keep the data of a hospital. Hospitals consist data such as city, capacity, name, address etc. and as a primary key it has a parameter named as hodpitalId which is choosen to be serial in order to avoid conflicts. HospitalInfo table includes add_hospital, update_hospital, delete_hospital and show_hospital_info methods. In this project, hospital informations can be modified only by admin.


:1) Creating HospitalInfo Table:

The code below represent creation of hospitalinfo table. This table includes a primary key named HospitalId which is serial in order to avoid conflicts when adding new hospitals to database and a foreign key names city which reference comes from ParameterInfo table. Also it includes non-key elements such as capacity, name, address and date of creation. Create_tables function can be found in database.py.

.. code-block:: python
   
   query = """DROP TABLE IF EXISTS HospitalInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE HospitalInfo (
                         HospitalID SERIAL PRIMARY KEY,
                         City INT NOT NULL,
                         Capacity INT NOT NULL,
                         Address VARCHAR(500) NOT NULL,
                         Name VARCHAR(250) NOT NULL,
                         CreateDate TIMESTAMP NOT NULL,
                         FOREIGN KEY (City) REFERENCES ParameterInfo(ID) ON DELETE CASCADE
                                                 )"""
            cursor.execute(query)


:2) Add Hospital:

The code below represent method of adding a new hospital to the database. It simply inserts a new row with the given attributes to hospitalInfo table. As the creation date of the hospital, it takes the current time depending on when the hospital is added to the database. Add_hospital method can be found in hospital.py.

.. code-block:: python

   @classmethod
    def add_hospital(cls, city, capacity, address, name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO HospitalInfo(City, Capacity, Address, Name, CreateDate) VALUES (%s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, (str(city), str(capacity), str(address), str(name), datetime.datetime.now()))
            except dbapi2.Error:
                connection.rollback()
                return -1
            else:
                connection.commit()
            cursor.close()
            return 1


:3) Update Hospital:

Similarly to add hospital method, update hospital method gives opportunity to modify an already added hospital. Differently from adding hospital, when updating, the hospital id which is a serial primary key in the table does not change, all the non-key elements can be changed and the creation date also updates itself to the time of updateing process. Update_hospital can be found under hospital.py.

.. code-block:: python

   @classmethod
    def update_hospital(cls, hospitalid, city, capacity, address, name):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = 'UPDATE HospitalInfo SET UpdateDate = ' + "'" + str(datetime.datetime.now()) + "'"

            if city != '' and city is not None:
                query = query + ", city = '" + str(city) + "'"
            if capacity != '' and capacity is not None:
                query = query + ", Capacity = '" + str(capacity) + "'"
            if address != '' and address is not None:
                query = query + ", address = '" + str(address) + "'"
            if name != '' and name is not None:
                query = query + ", Name = '" + str(name) + "'"
            query = query + ' WHERE HospitalId = ' + str(hospitalid)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return


:4) Delete Hospital:

Delete hospital info method, deletes the hospital given its hospitalId. Since in the create table it says ON DELETE CASCADE, it deletes itself from the connected tables too. Delete hospital info method can be found under hospital.py.

.. code-block:: python

   @classmethod
    def delete_hospital_info(cls, hospitalId):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM HospitalInfo WHERE HospitalID = %s"""
            try:
                cursor.execute(query, (hospitalId))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            return


:5) Connection to HTML:

To redirect to the hospital page the following piece of code is written. if the entered parameters are valid, it adds the hospital to the database easily from a userfriendly interface. The User Interface will be shown in User part of the report.

.. code-block:: python

   @site.route('/hospital', methods=['GET', 'POST'])
    def hospital_page():
    derror = "OK"
    if request.method=='POST':
        hospital = HospitalDatabase()
        hospitalAddCheck = hospital.add_hospital(city=request.form['City'], capacity=request.form['Capacity'], address=request.form['Address'], name=request.form['Name'])

        if hospitalAddCheck is None or hospitalAddCheck == -1:
            derror = 'Hospital could not be added'
        else:
            derror = 'Hospital is added'
        return render_template("hospital.html", derror=derror)
    else:
        return render_template("hospital.html")


Similarly to the code above, updating the hospital info can be done by the help of update_hospital page which is reached by:

.. code-block:: python

   @site.route('/updatehospital/<int:HospitalID>')
    def updaterehospital_page(HospitalID):
    derror = "OK"
    if request.method=='POST':
        create_hospital = HospitalDatabase()
        hospitalAddCheck = create_hospital.update_hospital(hospitalid=HospitalID, city=request.form['City'], capacity=request.form['Capacity'], address=request.form['Address'], name=request.form['Name'])
        if hospitalAddCheck is None or hospitalAddCheck == -1:
            derror = 'Hospital info could not be updated.'
        else:
            derror = 'Hospital info is updated'
        return render_template("updatehospital.html", derror=derror)
    else:
        return render_template("updatehospital.html")


DepartmentInfo Table & Methods
------------------------------

:1) Creating DepartmentInfo Table:

The code below represent creation of departmentinfo table. This table includes a primary key named DepartmentId which is serial in order to avoid conflicts when adding new departments to database and foreign keys named as hospitalId which reference comes from HospitalInfo table, and departmentTypeId which reference comes from ParameterInfo table. Also it includes non-key elements such as roomCount, blockNumber, personalCount and date of creation. Create_tables function can be found in database.py.

.. code-block:: python

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
                         FOREIGN KEY (HospitalID) REFERENCES HospitalInfo(HospitalID) ON DELETE CASCADE,
                         FOREIGN KEY (DepartmentTypeID) REFERENCES ParameterInfo(ID) ON DELETE RESTRICT
                                                   )"""
            cursor.execute(query)


:2) Adding Department:

The code below represent method of adding a new department to the database. It simply inserts a new row with the given attributes to departmentInfo table. As the creation date of the department, it takes the current time depending on when the department is added to the database. add_department method can be found in department.py.

.. code-block:: python

   @classmethod
    def add_department(cls, hospitalid, deptypeid, roomcount, blocknumber, personalcount):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO DepartmentInfo(HospitalID, DepartmentTypeID, RoomCount, BlockNumber, PersonalCount, CreateDate) VALUES (%s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, str(hospitalid), str(deptypeid), str(roomcount), str(blocknumber), str(personalcount), datetime.datetime.now())
            except dbapi2.Error:
                connection.rollback()
                return -1
            else:
                connection.commit()
            cursor.close()
            return 1


:3) Update Department:

Similarly to add department method, update department method gives opportunity to modify an already added department. Differently from adding department, when updating, the department id which is a serial primary key in the table does not change, all the non-key elements can be changed and the creation date also updates itself to the time of updateing process. Update_department can be found under department.py.

.. code-block:: python

   @classmethod
    def update_department(cls, departmentid, hospitalid, departmentTypeid, roomCount, blockNumber, personalCount):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = 'UPDATE DepartmentInfo SET UpdateDate = ' + "'" + str(datetime.datetime.now()) + "'"

            if hospitalid != '' and hospitalid is not None:
                query = query + ", HospitalId = '" + str(hospitalid) + "'"
            if departmentTypeid != '' and departmentTypeid is not None:
                query = query + ", DepartmentTypeId = '" + str(departmentTypeid) + "'"
            if roomCount != '' and roomCount is not None:
                query = query + ", RoomCount = '" + str(roomCount) + "'"
            if blockNumber != '' and blockNumber is not None:
                query = query + ", BlockNumber = '" + str(blockNumber) + "'"
            if personalCount != '' and personalCount is not None:
                query = query + ", PersonalCount = '" + str(personalCount) + "'"
            query = query + 'WHERE DepartmentId = ' + str(departmentid)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return


:4) Delete Department:

Delete department info method, deletes the department given its departmentId. Since in the create table it says ON DELETE CASCADE for the departmentId, it deletes itself from the connected tables too. Differently, for hospitalId element is says ON DELETE RESTRICT, in the deletion of department, hospital wants to be deleted too, it does not let that to happen. Delete department info method can be found under department.py.

.. code-block:: python

  @classmethod
    def delete_department_info(cls, departmentId):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM DepartmentInfo WHERE DepartmentID = %s"""
            try:
                cursor.execute(query, (departmentId))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            return


:5) Connection to HTML:

To redirect to the department page the following piece of code is written. if the entered parameters are valid, it adds the department to the database easily from a userfriendly interface. The User Interface will be shown in User part of the report.

.. code-block:: python

   @site.route('/department', methods=['GET', 'POST'])
    def department_page():
    derror = "OK"
    if request.method=='POST':
        department = DepartmentDatabase()
        departmentAddCheck = department.add_department(hospitalid=request.form['HospitalID'], deptypeid=request.form['DepartmentTypeID'], roomcount=request.form['RoomCount'], blocknumber=request.form['BlockNumber'], personalcount=request.form['PersonalCount'])

        if departmentAddCheck is None or departmentAddCheck == -1:
            derror = 'Department could not be added'
        else:
            derror = 'Department is added'
        return render_template("department.html", derror=derror)
    else:
        return render_template("department.html")


Similarly to the code above, updating the department info can be done by the help of update_department page which is reached by:

.. code-block:: python

   @site.route('/updatedepartment/<int:DepartmentID>')
    def updatedepartment_page(DepartmentID):
    derror = "OK"
    if request.method=='POST':
        create_department = DepartmentDatabase()
        departmentAddCheck = create_department.update_department(departmentid=DepartmentID, hospitalid=request.form['HospitalID'], departmentTypeid=request.form['DepartmentTypeID'], roomCount=request.form['RoomCount'], blockNumber=request.form['BlockNumber'], personalCount=request.form['PersonalCount'])
        if departmentAddCheck is None or departmentAddCheck == -1:
            derror = 'Department info could not be updated.'
        else:
            derror = 'Department info is updated'
        return render_template("updatedepartment.html", derror=derror)
    else:
        return render_template("updatedepartment.html")


RoomInfo Table & Methods
------------------------

:1) Creating RoomInfo Table:

The code below represent creation of roominfo table. This table includes a primary key named RoomId which is serial in order to avoid conflicts when adding new rooms to database and a foreign key named as departmentId which reference comes from DepartmentInfo table. Also it includes non-key elements such as roomNo, bathroomCount, capacity, date of creation and update date. Create_tables function can be found in database.py.

.. code-block:: python

   query = """DROP TABLE IF EXISTS RoomInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE RoomInfo (
                         DepartmentID INT,
                         RoomNo INT NOT NULL,
                         RoomID SERIAL PRIMARY KEY,
                         Capacity INT NOT NULL,
                         BathroomCount INT,
                         LastControl TIMESTAMP,
                         CreateDate TIMESTAMP NOT NULL,
                         UpdateDate TIMESTAMP,
                         FOREIGN KEY (DepartmentID) REFERENCES DepartmentInfo(DepartmentID) ON DELETE CASCADE
                                             )"""
            cursor.execute(query)


:2) Adding Room:

The code below represent method of adding a new room to the database. It simply inserts a new row with the given attributes to RoomInfo table. As the creation date of the room, it takes the current time depending on when the room is added to the database. add_room method can be found in department.py.

.. code-block:: python

   @classmethod
    def add_room(cls, departmentid, roomno, capacity, bathroomcount):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO RoomInfo(DepartmentID, RoomNo, Capacity, BathroomCount, LastControl, CreateDate, UpdateDate) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            try:
                cursor.execute(query, str(departmentid), str(roomno), str(capacity), str(bathroomcount), datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now())
            except dbapi2.Error:
                connection.rollback()
                return -1
            else:
                connection.commit()
            cursor.close()
            return 1


:3) Update Room:

Similarly to add room method, update room method gives opportunity to modify an already added room. Differently from adding room, when updating, the room id which is a serial primary key in the table does not change, all the non-key elements can be changed and the creation date remains same but in this table it adds an attribute named update time which shows the time of updateing process. Update_room can be found under room.py.

.. code-block:: python

   @classmethod
    def update_room(cls, roomid, departmentid, roomno, capacity, bathroomCount):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = 'UPDATE RoomInfo SET UpdateDate = ' + "'" + str(datetime.datetime.now()) + "'"

            if departmentid != '' and departmentid is not None:
                query = query + ", DepartmentId = '" + str(departmentid) + "'"
            if roomno != '' and roomno is not None:
                query = query + ", RoomNo = '" + str(roomno) + "'"
            if capacity != '' and capacity is not None:
                query = query + ", Capacity = '" + str(capacity) + "'"
            if bathroomCount != '' and bathroomCount is not None:
                query = query + ", BathroomCount = '" + str(bathroomCount) + "'"
            query = query + ' WHERE RoomId = ' + str(roomid)

            try:
                cursor.execute(query)
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()
            return


:4) Delete Room:

Delete room info method, deletes the room given its roomId. Since in the create table it says ON DELETE CASCADE for the departmentId, it deletes itself automatically if the department is deleted. Delete room info method can be found under room.py.

.. code-block:: python

   def delete_room_info(cls, roomId):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """DELETE FROM RoomInfo WHERE RoomID = %s"""
            try:
                cursor.execute(query, (roomId))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            return


:5) Connection to HTML:

To redirect to the room page the following piece of code is written. if the entered parameters are valid, it adds the room to the database easily from a userfriendly interface. The User Interface will be shown in User part of the report.

.. code-block:: python

   @site.route('/room', methods=['GET', 'POST'])
    def room_page():
    derror = "OK"
    if request.method=='POST':
        room = RoomDatabase()
        roomAddCheck = room.add_room(departmentid=request.form['DepartmentID'], roomno=request.form['RoomNo'], capacity=request.form['Capacity'], bathroomcount=request.form['BathroomCount'])

        if roomAddCheck is None or roomAddCheck == -1:
            derror = 'Room could not be added'
        else:
            derror = 'Room is added'
        return render_template("room.html", derror=derror)
    else:
        return render_template("room.html")


Similarly to the code above, updating the room info can be done by the help of update_room page which is reached by:

.. code-block:: python

   @site.route('/updateroom/<int:RoomID>')
    def updaterederoom_page(RoomID):
    derror = "OK"
    if request.method=='POST':
        create_room = RoomDatabase()
        roomAddCheck = create_room.update_room(roomid=RoomID, departmentid=request.form['DepartmentID'], roomno=request.form['RoomNo'], capacity=request.form['Capacity'], bathroomCount=request.form['BathroomCount'])
        if roomAddCheck is None or roomAddCheck == -1:
            derror = 'Room info could not be updated.'
        else:
            derror = 'Room info is updated'
        return render_template("updateroom.html", derror=derror)
    else:
        return render_template("updateroom.html")


ParameterInfo Table
-------------------

:Creating ParameterInfo Table:

The ParameterInfo Table is a helping table for many main tables in out project. the ID which is a serial primary key connect to hospital id, department id and room id. Similarly Type id connects to department type id and the name parameter keeps the names of these different types of ID's connected to other tables. The code below represent the creation of the ParameterInfo Table. It can be found under database.py.

.. code-block:: python

   query = """DROP TABLE IF EXISTS ParameterInfo CASCADE """
            cursor.execute(query)
            query = """CREATE TABLE ParameterInfo (
                         ID SERIAL PRIMARY KEY,
                         TypeID INT NOT NULL,
                         Name VARCHAR(100) NOT NULL,
                         FOREIGN KEY (TypeID) REFERENCES ParameterType(ID) ON DELETE RESTRICT
                                                  )"""
            cursor.execute(query)