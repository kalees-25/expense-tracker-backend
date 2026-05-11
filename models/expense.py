# expenses = []    #-> temporary storage


from sqlalchemy import Column, Integer, String, Numeric  , DateTime , Date

from datetime import datetime

from database.connection import Base



class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer,
                  primary_key=True, 
                  autoincrement=True,
    )
    
    date = Column(Date,
    nullable=False

    )
    category = Column(String(100),
                       nullable=False
    )
    
    description = Column(String(255),
                          nullable=False
    )

    amount = Column(Numeric(10,2),
                     nullable=False
    )


    created_at = Column(
     DateTime,
     default=datetime.utcnow,
     nullable=False
)


    updated_at = Column(
    DateTime,
    default= datetime.utcnow,
    onupdate=datetime.utcnow,
    nullable=False
   

)