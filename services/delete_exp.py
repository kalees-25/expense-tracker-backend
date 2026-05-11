from fastapi import HTTPException , status  

from sqlalchemy.orm import Session


from models.expense import Expense




# def delete_expense(id: int):

#     for index, expense in enumerate(expenses):

#         if expense["id"] == id:
          
#         #   POP  -> REMOVE AND RETURN THE ITEM
#             deleted_expense = expenses.pop(index)

#             return {"message": "Expense deleted successfully", 
#                     "deleted": deleted_expense}

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                          detail="Expense not found")



def delete_expense(expense_id: int , db: Session):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            
              detail="Expense not found")

    try:

        db.delete(expense)

        db.commit()

        return {
             "message": "Expense deleted successfully"
        }

    except Exception:

        db.rollback()
    
        db.delete()

        raise
