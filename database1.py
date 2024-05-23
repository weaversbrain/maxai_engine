from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv() # 환경변수 읽어오기

DB_URL = os.getenv('MYSQL_MAXAI')

engine = create_engine(DB_URL, pool_recycle = 500)   # DB 커넥션 풀 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)    # DB접속을 위한 클래스
 
Base = declarative_base()    # Base 클래스는 DB 모델 구성할 때 사용

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()