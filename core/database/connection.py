from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session


#-----------------ENVIRONMENT VARIABLE------------------
from dotenv import load_dotenv
import os



# ------------READ ENVIRONMENT VARIABLE----------------
load_dotenv()

# -----------------ENVIRONMENT VARIABLE  ----------------

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")



# --------------------------ACCESS ENVIRONMENT VARIABLE-------------------------------
DATABASE_URL = (f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)         


engine = create_engine(DATABASE_URL ,
                       pool_pre_ping=True
                       )



SessionLocal = sessionmaker(
     bind=engine,
     
     autocommit=False,
    
     autoflush=False,
)

Base = declarative_base()

def get_db():

# ----- SESSION ->TYPE HINT ------------------------------- 
    db:Session = SessionLocal()

    try:
        yield db

    finally:
        db.close()

