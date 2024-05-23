from database import Database
import random

if __name__ == "__main__":

    # postqresql 테스트
    db = Database('postqresql')
    #db.insertDB(table='table',colum='ID',data='유동적변경')
    print(db.readDB(table='PUBLIC.\"Prompt\"',colum='name'))
    #db.updateDB(table='table',colum='ID', value='와우',condition='유동적변경')
    #db.deleteDB(table='table',condition ="id != 'd'")


    # mysql 테스트
    db = Database('mysql')
    #db.insertDB(table='Board',colum='writer,title,cclontent',data="'test','테스트입니다','test"+str(random.randrange(1,999))+"'")
    print(db.readDB(table='Board',colum='writer,title,content'))
    #db.updateDB(table='Board',colum='ID', value='와우',condition='유동적변경')
    #db.deleteDB(table='Board',condition ="id != 'd'")
