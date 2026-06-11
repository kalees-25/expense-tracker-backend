import logging

from models.expense import Expense

from schemas.expense import ExpenseCreate  , ExpenseUpdate

from sqlalchemy.orm import Session

from sqlalchemy.exc import SQLAlchemyError

from fastapi import HTTPException, status



from sqlalchemy import asc, desc, func
from schemas.expense import ExpenseQueryParams
import math
# -------------------------------------
    # ------------------LOGGER CONFIGURATION----------------
logger = logging.getLogger(__name__)           
# ------------------------------------------



# --------------------GET ALL EXPENSES-------------------------------
def get_all_expenses(db: Session):
    logger.info("Fetching all expenses")
    try:
        # DB EXPENSES TABLE ALL ITEMS GET THE DATA AND GIVEN TO PYTHON OBJECT
        expenses = db.query(Expense).all()
        return expenses
    except SQLAlchemyError as e:  
        logger.exception(f"Database fetch failed | error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
        



# ---------------------------------------------------
# CREATE EXPENSE
# ---------------------------------------------------

def add_expense(
    db: Session,  # TO CREATE FUNCTION FOR ADDING NEW EXPENSE, DATA
    data: ExpenseCreate ,
    user_id: int
):          
    logger.info("Create expense request received for user_id=%s", user_id)

    #--------------------CREATE NEW OBJECT--------------------------
    new_expense = Expense(
        date=data.date,
        
        category=data.category,
        
        description=data.description,
        
        amount=data.amount ,
        # DATA OBJECT INSIDE ACCESS THE DATA FIELD
        user_id=user_id
    )

    try:
        logger.info("Adding expense to database")
        db.add(new_expense)
        db.commit()

        # ---- IN DB LATEST CHANGES GET RETURNED AS PYTHON OBJECT
        db.refresh(new_expense)

        logger.info(
            f"Expense created successfully | "
            
            f"expense_id=%s |"
            
            f"user_id=%s", 
            
            new_expense.id, user_id
            
        )
        return new_expense

    except SQLAlchemyError as e:
        # ----- CLEANS THE FAILED TRANSACTION
        db.rollback()
        logger.exception(
            f"Expense creation failed | "
            f"error={str(e)}"
        )

        # RE-RAISE CURRENT EXCEPTION
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
        
        
        
        # ------------------------------------------------
        # ---------------- AG-GRID CONFIGURATION ----------------
        # ------------------------------------------------
def get_user_expenses(
    db: Session,
    user_id: int,
    params: ExpenseQueryParams
):

    query = db.query(Expense).filter(
        Expense.user_id == user_id
    )

    # Search

    if params.search:

        query = query.filter(
            Expense.description.ilike(
                f"%{params.search}%"
            )
        )

    # Category Filter

    if params.category:

        query = query.filter(
            Expense.category == params.category
        )

    # Total Count

    total = query.count()

    # Sorting

    allowed_sorts = {
        "id": Expense.id,
        "date": Expense.date,
        "amount": Expense.amount,
        "category": Expense.category,
        "description": Expense.description
    }

    sort_column = allowed_sorts.get(
        params.sort_by,
        Expense.id
    )

    if params.sort_order.lower() == "asc":

        query = query.order_by(
            asc(sort_column)
        )

    else:

        query = query.order_by(
            desc(sort_column)
        )

    # Pagination

    offset = (
        params.page - 1
    ) * params.page_size

    items = (
        query
        .offset(offset)
        .limit(params.page_size)
        .all()
    )

    total_pages = (total + params.page_size - 1 ) // params.page_size if params.page_size else 0

    return {
        "items": items,
        "total": total,
        "total_pages":total_pages,
       
    }
    
    
    
    # ================================================================================
                    #    GET SINGLE Expense
    # ================================================================================
    
def get_expense_by_id(
    id: int,
    db: Session,
    user_id: int
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == id,
            Expense.user_id == user_id
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return expense