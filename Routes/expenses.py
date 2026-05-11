from fastapi import APIRouter , Depends ,status

from services.expenses import (
    get_all_expenses , add_expense
)

from schemas.expense import ExpenseCreate , ExpenseResponse

from database.connection import get_db

from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
    responses={404: {"description": "Not found"}}
)

# ----------------------ROUTES-----------------------

# --------------------GET ALL EXPENSE ---------------------
@router.get("/"  ,
            response_model=list[ExpenseResponse] ,
             status_code=status.HTTP_200_OK
) 


def get_expenses(
    db:Session = Depends(get_db)

):        #   : -> IN THIS FUNCTION WE WILL RETURN A INDENTED LINES ,ALL ARE IN THIS FUNCTION return get_all_expenses()
    
    return get_all_expenses(db)


# ----------------------------- CREATE EXPENSE ----------------------------------


@router.post("/" ,
             response_model = ExpenseCreate,
             status_code=status.HTTP_201_CREATED

)


def create_expenses(expense_data:ExpenseCreate , 
                    db:Session = Depends(get_db)

):
    
    return add_expense(db,expense_data )


