import os
import psycopg2

class HerokuCnx():
    def __init__(self):
        self.cnx = self.conn()

    @staticmethod
    def conn():
        return psycopg2.connect(os.environ['RALSTON_DB_URL'])
