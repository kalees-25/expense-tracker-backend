from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.expense import Expense
from schemas.expense import ExpenseUpdate


def update_expense(id: int, 
                   updated_data: ExpenseUpdate,
                    db:Session):
    expense = db.query(Expense).filter(Expense.id == id).first()

    
    if not expense: # pyright: ignore[reportUndefinedVariable]
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

        return expense

    except Exception:
        
        db.rollback()
        
        raise





