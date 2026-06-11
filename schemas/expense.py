
from pydantic import BaseModel, Field, field_validator, ConfigDict 

from datetime import date

from typing import Literal , List



# -------------------------------------------------
# CATEGORY TYPE
# -------------------------------------------------

ExpenseCategory = Literal[
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Health",
    "Entertainment",
    "Rent",
    "Working",
    "Loan"
]


# -------------------------------------------------
# CREATE SCHEMA
# -------------------------------------------------

class ExpenseBase(BaseModel):

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


    @field_validator("description")
    @classmethod
    def clean_description(cls, value):

        value = value.strip()

        if not value:
            raise ValueError(
                "Description cannot be empty"
            )

        return value


# -------------------------------------------------
# UPDATE SCHEMA
# -------------------------------------------------

class ExpenseCreate(ExpenseBase):
    pass
    

class ExpenseUpdate(
    ExpenseBase
):
    pass



# -------------------------------------------------
# RESPONSE SCHEMA
# -------------------------------------------------

class ExpenseResponse(BaseModel):

    id: int

    date: date

    category: ExpenseCategory

    description: str

    amount: float


    model_config = ConfigDict(from_attributes=True)


class ExpenseQueryParams(
    BaseModel
):

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    search: str | None = None

    category: ExpenseCategory | None = None

    sort_by: Literal[
        "id",
        "date",
        "category",
        "description",
        "amount",
    ] = "date"

    sort_order: Literal[
        "asc", 
        "desc"
    ] = "desc"
     
     
     
class ExpenseListResponse(BaseModel):

    items: List[ExpenseResponse]

    total: int
    
    total_pages: int
    
  
    