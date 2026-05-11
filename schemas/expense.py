from pydantic import BaseModel , Field , field_validator

from datetime import date 

from sqlalchemy import Numeric

from typing import Literal



# ----------------------REQUEST SCHEMA-----------------------
class ExpenseCreate(BaseModel):
    date:date

    category:str = Literal[
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Health",
        "Entertainment"
    ]

    description:str =Field(...,
        min_length=3,
        max_length=100,
        pattern = r"^[a-zA-Z0-9\s.,()-]+$"

    )

    amount:Numeric = Field(...,
        gt=0,
        lt=10000000
    )


# ----------------------UPDATE SCHEMA-----------------------
class ExpenseUpdate(BaseModel):
    
      date:date

category:str = Literal[
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Health",
        "Entertainment"
    ]

description:str =Field(...,
        min_length=3,
        max_length=100,
        pattern = r"^[a-zA-Z0-9\s.,()-]+$"

    )

amount:Numeric = Field(...,
        gt=0,
        lt=10000000
    )

# ----------------------RESPONSE SCHEMA-----------------------
class ExpenseResponse(BaseModel):
    date:date

    category:str = Literal[
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Health",
        "Entertainment"
    ]

    description:str =Field(...,
        min_length=3,
        max_length=100,
        pattern = r"^[a-zA-Z0-9\s.,()-]+$"

    )

    amount:Numeric = Field(...,
        gt=0,
        lt=10000000
    )


#----------------DESCRIPTION VALIDATION---------------------

@field_validator("description")
@classmethod
def clean_description(cls, value):

    value = value.strip()

    if not value:
         raise ValueError("Description cannot be empty")

    return value


#  
class Config:
    from_attributes = True 

#-----------IN OBJECT ARE ALSO CONVERT IN TO JSON DATA----------------