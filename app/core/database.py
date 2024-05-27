"""
+----------------------------------------------------------------------+
| Copyright (c) 2024 WEAVERSBRAIN. co. Ltd
+----------------------------------------------------------------------+
| 작업일 : 2024-05-23
| 파일설명 : 
+----------------------------------------------------------------------+
| 작업자 : koreanred
+----------------------------------------------------------------------+
| 수정이력
|
+----------------------------------------------------------------------+ 
"""

import psycopg2 #postqresql
import pymysql  #mysql
from dotenv import dotenv_values

config = dotenv_values(".env") # 환경변수 읽어오기

class Database():
    def __init__(self, gubun):

        if gubun == 'postqresql':
            self.db = psycopg2.connect(host=config['POSTQRESQL_HOST'], dbname=config['POSTQRESQL_DB'],user=config['POSTQRESQL_USER'],password=config['POSTQRESQL_PASSWD'],port=config['POSTQRESQL_PORT'])

        elif gubun == 'mysql':
            self.db = pymysql.connect(host=config['MYSQL_MAXAI_B2B_HOST'], port=int(config['MYSQL_MAXAI_B2B_PORT']), user=config['MYSQL_MAXAI_B2B_USER'], passwd=config['MYSQL_MAXAI_B2B_PASSWD'], db=config['MYSQL_MAXAI_B2B_DB'], charset=config['MYSQL_MAXAI_B2B_CHARSET'])

        if self.db:
            self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.cursor.commit()
       
    def insertDB(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor.lastrowid    
        except Exception as e :
            print(" insert DB  ",e)
 
    def readDB(self,sql,type='one'):
        try:
            self.cursor.execute(sql)
            if type == 'one' :
                result = self.cursor.fetchone()
            else:
                result = self.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
        
        return result

    def updateDB(self,sql):
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" update DB err",e)

    def deleteDB(self,sql):
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print( "delete DB err", e)
