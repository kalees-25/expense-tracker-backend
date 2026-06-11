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


# -------------------------------------------------
# UPDATE SCHEMA
# -------------------------------------------------

class ExpenseUpdate(BaseModel):

    date: date

    category: ExpenseCategory

    description: str = Field(
        ...,
        min_length=3,
        max_length=100,
        pattern=r"^[a-zA-Z0-9\s,.()-]+$"
    )

    amount: float = Field(
        ...,
        gt=0,
        lt=1000000
    )

    user_id: int


# -------------------------------------------------
# RESPONSE SCHEMA
# -------------------------------------------------

class ExpenseResponse(BaseModel):

    id: int

    date: date

    category: ExpenseCategory

    description: str

    amount: float

    user_id: int


    model_config = ConfigDict(from_attributes=True)