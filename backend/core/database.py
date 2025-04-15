from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# MySQL 连接地址
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:118211yao@localhost:3306/travel_agency?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
