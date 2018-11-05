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