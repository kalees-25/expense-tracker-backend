from fastapi import APIRouter , status, Depends

from schemas.expense import ExpenseUpdate , ExpenseResponse

from services.update_exp  import update_expense

from services.delete_exp import delete_expense


from services.expenses import get_expense_by_id


from sqlalchemy.orm import Session

from core.database.connection import get_db


from models.users import User


from core.security import get_current_user



    # --------------------------------------------------------
    #                    LOGGER INFO
    # ----------------------------------------------------------
from core.logger import logger



router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

#---------------------- UPDATE EXPENSE-----------------------------------
@router.put("/{id}",
             response_model=ExpenseResponse , 
             status_code = status.HTTP_200_OK
)


def update_expense_route(id: int , 
                         expense_data: ExpenseUpdate , 
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)


):
        # --------------------------------------------------------
    #                    LOGGER INFO
    # ----------------------------------------------------------
    logger.info(
    "Update expense request received | expense_id=%s | user_id=%s",
    id,
    current_user.id
)
    return update_expense(id, expense_data , db , current_user.id)



# -----------------------  UPDATE EXPENSE --------------------------------

@router.get(
    "/{id}",
    response_model=ExpenseResponse,
    status_code=status.HTTP_200_OK
)
def get_expense_route(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_expense_by_id(
        id=id,
        db=db,
        user_id=current_user.id
    )




# ------------------------DELETE EXPENSE-------------------------------------
@router.delete("/{id}" )
def delete_expense_route(id:int , 
                         db:Session  = Depends(get_db),
                         current_user: User = Depends(get_current_user)

):
        # --------------------------------------------------------
    #                    LOGGER INFO
    # ----------------------------------------------------------
    logger.info("DELETE / Expenses request received")
    return delete_expense(id , db , current_user.id)
