import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database.connection import get_db

from core.security import get_current_user

from models.users import User

from schemas.expense import (
    ExpenseCreate,
    ExpenseResponse,
    ExpenseQueryParams,
    ExpenseListResponse
)

from services.expenses import (
    get_user_expenses,
    add_expense
)


# ------------AG-GRID API------------------------------------
from typing import Annotated

from services.expenses import (
    get_user_expenses
)



# ---------------------------------------------------
# LOGGER
# ---------------------------------------------------

logger = logging.getLogger(__name__)


# ---------------------------------------------------
# ROUTER
# ---------------------------------------------------

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)



# ---------------------------------------------------
#                CREATE EXPENSE
# ---------------------------------------------------

@router.post(
    "/",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED
)
@router.post("/", response_model=ExpenseResponse, status_code=201)
def create_expense(
    expense_data: ExpenseCreate,          # Request body
    db: Session = Depends(get_db),        # DB connection
    current_user: User = Depends(get_current_user)  # Auth
):

    logger.info(
        "POST /expenses request received | user_id=%s",
        current_user.id
    )

    return add_expense(
        db=db,
        data=expense_data,
        user_id=current_user.id
    )
    
    
    # ---------------------------------------------------
    #             AG-GRID  API
    # ---------------------------------------------------
    


@router.get(
    "/",
    response_model=
    ExpenseListResponse,
    status_code=status.HTTP_200_OK
)
def list_expenses(

    params: Annotated[         # ANNOTATED => NORMAL DATA TYPE + EXTRA RULES
            
        ExpenseQueryParams,
        Depends()
    ],

    db: Session = Depends(
        get_db
    ),

    current_user: User =
    Depends(
        get_current_user
    ),

):

    logger.info(
        "GET /expenses | "
        "user_id=%s",
        current_user.id
    )

    return get_user_expenses(
        db=db,
        user_id=current_user.id,
        params=params,
    )