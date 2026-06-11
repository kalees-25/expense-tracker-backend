import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.expense import Expense
from schemas.expense import ExpenseUpdate

from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

def update_expense(
                expense_id:int, 
                
                updated_data: ExpenseUpdate,
                
                db:Session,
                
                user_id:int
                
                ):
    expense = (
    db.query(Expense)
    .filter(
        Expense.id == expense_id,
        Expense.user_id == user_id
    )
    .first()
)

    
    if not expense:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
          detail="Expense not found")

    expense.date = updated_data.date
    expense.category = updated_data.category
    expense.description = updated_data.description
    expense.amount = updated_data.amount
   

    try:
        db.commit()

        db.refresh(expense)
        
        logger.info(
            "Expense updated successfully | expense_id=%s | user_id=%s",
            expense_id,
            user_id
        )

        return expense

    except SQLAlchemyError:
        
        db.rollback()
        
        logger.exception("Expense update failed | expense_id=%s | user_id=%s",
                         expense_id , user_id
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )




