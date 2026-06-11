from sqlalchemy import Column, Index, Integer, String, Numeric, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from core.database.connection import Base


# --------------------------------------------------------
#                     EXPENSE MODEL
# --------------------------------------------------------
class Expense(Base):

    __tablename__ = "expenses"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    date = Column(
        Date,
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False
    )

    description = Column(
        String(255),
        nullable=False
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="expenses"
    )
    
    
# =========================================================
#                      AG-GRID
# =========================================================


    __table_args__ = (

        Index(
             "idx_expense_user",
            "user_id"
        ),

        Index(
            "idx_expense_user_category",
            "user_id",
            "category"
        ),

        Index(
            "idx_expense_user_date",
            "user_id",
            "date"
        ),

)