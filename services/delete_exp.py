from fastapi import HTTPException , status  

from sqlalchemy.orm import Session

from models.expense import Expense

from  sqlalchemy.exc import SQLAlchemyError


from core.logger import logger



def delete_expense(expense_id:int ,
                 
                   db: Session , 
                   
                   user_id:int
                
                   ):

    logger.info(f"Deleting expense request received |expense_id=%s | user_id=%s" ,
                expense_id , user_id
                )
    

    expense =(

     db.query(Expense).filter(
         Expense.id == expense_id , 
         Expense.user_id == user_id
         )  
    .first()

    )

    if not expense:

        logger.warning(f"Expense not found | expense_id ={expense_id} | user_id={user_id}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
                            
            detail="Expense not found"
        )

    try:
          
        logger.info(
                "Deleting expense from database | expense_id=%s",
                 expense_id)

        db.delete(expense)

        db.commit()
        
        logger.info(
            "Expense deleted successfully | expense_id=%s | user_id=%s",
            
            expense_id,
            
            user_id
        )

        return {
             "success": True,
             "message": "Expense deleted successfully"
        }

    except SQLAlchemyError as e:
        db.rollback()
    
        logger.exception (
            "Expense delete failed | expense_id=%s | user_id=%s",
            expense_id,
            user_id
        )
        
        

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
