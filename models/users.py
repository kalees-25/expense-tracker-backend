from sqlalchemy import Column, Integer, String ,DateTime

from sqlalchemy.orm import relationship

from datetime import datetime

from core.database.connection import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    username = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    
    hashed_password = Column(
        String(255),
        nullable=False
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    expenses = relationship(

        "Expense",

        back_populates="user",

        cascade="all, delete"

    )