from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session


#-----------------ENVIRONMENT VARIABLE------------------
from dotenv import load_dotenv
import os



# ------------READ ENVIRONMENT VARIABLE----------------
load_dotenv()



# --------------------------ACCESS ENVIRONMENT VARIABLE-------------------------------
DATABASE_URL =os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)



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

