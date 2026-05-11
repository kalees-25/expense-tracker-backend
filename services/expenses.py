
from models.expense import Expense

from schemas.expense import ExpenseCreate , ExpenseUpdate

from sqlalchemy.orm import Session

def get_all_expenses(db:Session):
    # DB EXPENSES TABLE  ALL ITEMS GET  THE DATA AND GIVEN TO PYTHON OBJECT
    return db.query(Expense).all()

def add_expense(db:Session ,    # TO CREATE FUNCTION FOR ADDING NEW EXPENSE  , DATA
                data:ExpenseCreate
 ):          
    
#--------------------CREATE NEW OBJECT--------------------------
    new_expense = Expense(
  
        date = data.date,
        category =  data.category,
        description =  data.description,
        amount = data.amount
      # DATA OBJECT INSIDE ACCESS THE DATA FIELD
    )

    try:
        db.add(new_expense)

        db.commit()

        # ----IN DB LATEST CHANGES GET RETURNED AS PYTHON OBJECT
        db.refresh(new_expense)  

        return new_expense
 
    except Exception:

        # -----CLEANS THE FAILED TRANSACTION
        db.rollback()

        # RE-RAISE THE CUURENT EXCEPTION
        raise
