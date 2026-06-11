from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from models.expense import Expense
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


def get_dashboard_summary(
    db: Session,
    user_id: int
):

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .all()
    )
    
    #===================================================================================
    # Total Expense
    #===================================================================================

    total_expense = (
        db.query(func.sum(Expense.amount))
        .filter(
            Expense.user_id == user_id
    )
        .scalar()
    ) or 0
    
    #===================================================================================
    # Expense Count
    #===================================================================================
    expense_count = (
        db.query(func.count(Expense.id))
        .filter(
            Expense.user_id == user_id
    )
        .scalar()
)


    

      # HIGHEST EXPENSE
    highest_expense = (
        db.query(func.max(Expense.amount))
        .filter(
            Expense.user_id == user_id)
        .scalar()       # it handles sigle value return and respons
    ) or 0
    
    #===================================================================================
    # TOP CATEGORY EXPENSE
    #===================================================================================
    top_category = (
        db.query(
            Expense.category,
            func.sum(Expense.amount).label("total")
        )
        .filter(Expense.user_id == user_id)
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
        .first()
    )
    
    top_category_name = (
        top_category.category
        if top_category
        else "N/A"
    )
    
    # ===================================================================================
    # CATEGORY BREAKDOWN
    # ===================================================================================
    category_breakdown = (
        db.query(
            Expense.category,
            func.sum(
                Expense.amount
            ).label("total")
    )
        .filter(
            Expense.user_id == user_id
    )
        .group_by(
            Expense.category
    )
        .all()
)
    
    category_breakdown_data = [
           {
        "category": row.category,
        "amount": float(row.total)
    }
    for row in category_breakdown 
    ]
    
    # ===================================================================================
    # CURRENT MONTH TOTAL 
    # ===================================================================================
    
    current_month = datetime.now().month
    current_year = datetime.now().year

    current_month_total = sum(
        float(exp.amount)
        for exp in expenses
        if (
            exp.date.month == current_month
        and
        exp.date.year == current_year
   )
)
    
    #===================================================================================
    # RECENT EXPENSES
    #===================================================================================
    
    recent_expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
    )
        .order_by(
            Expense.date.desc()
    )
        .limit(5)
        .all()
)
    
    
    return {
        "total_expense": total_expense,
        "expense_count": expense_count,
        "highest_expense": highest_expense,
        "top_category": top_category_name,
        "current_month_total": current_month_total,
        "recent_expenses": recent_expenses,
        "category_breakdown": category_breakdown_data
    }