from fastapi import APIRouter , status, Depends

from schemas.expense import ExpenseUpdate , ExpenseResponse

from services.update_exp  import update_expense

from services.delete_exp import delete_expense

from sqlalchemy.orm import Session

from database.connection import get_db


    # --------------------------------------------------------
    #                    LOGGER INFO
    # ----------------------------------------------------------
from core.logger import logger



router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)

#---------------------- UPDATE EXPENSE-----------------------------------
@router.put("/{id}",
             response_model=ExpenseResponse , 
             status_code = status.HTTP_200_OK
)


def update_expense_route(id: int , 
                         expense_data: ExpenseUpdate , 
                         db: Session = Depends(get_db)

):
        # --------------------------------------------------------
    #                    LOGGER INFO
    # ----------------------------------------------------------
    logger.info("PUT / Expenses request received")  
    return update_expense(id, expense_data , db)



# ------------------------DELETE EXPENSE-------------------------------------
@router.delete("/{id}" )
def delete_expense_route(id:int , db:Session  = Depends(get_db)

):
        # --------------------------------------------------------
    #                    LOGGER INFO
    # ----------------------------------------------------------
    logger.info("DELETE / Expenses request received")
    return delete_expense(id , db)
