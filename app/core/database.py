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

    def insertDB(self,table,colum,data):
        sql = " INSERT INTO {table}({colum}) VALUES ({data}) ;".format(table=table,colum=colum,data=data)
        #print(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB  ",e)

    def readDB(self,table,colum):
        sql = " SELECT {colum} from {table}".format(colum=colum,table=table)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
        
        return result
    
    def readDBOne(self,table,colum):
        sql = " SELECT {colum} from {table}".format(colum=colum,table=table)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
        except Exception as e :
            result = (" read DB err",e)
        
        return result

    def readDBSql(self,sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
        
        return result
    
    def updateDB(self,table,colum,value,condition):
        sql = " UPDATE {table} SET {colum}='{value}' WHERE {colum}='{condition}' ".format(table=table , colum=colum ,value=value,condition=condition )
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" update DB err",e)

    def updateDBSql(self,sql):
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" update DB err",e)

    def deleteDB(self,table,condition):
        sql = " delete from {table} where {condition} ; ".format(table=table, condition=condition)
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print( "delete DB err", e)
