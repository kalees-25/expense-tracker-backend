from fastapi import FastAPI

#---------------------IMPORTING MIDDLEWARE-----------------
from middleware.cors import add_cors


from Routes.expenses  import router as expense_router

from Routes.put_del_exp import router as put_del_router

from Routes.auth import router as auth_router


from Routes.dashboard import router as dashboard_router


# ---------------------IMPORTING EXCEPTION HANDLER----------------
from core.exception_handler import (
    validation_exception_handler , 
    database_exception_handler ,
    generic_exception_handler
)

from fastapi.exceptions import RequestValidationError

from sqlalchemy.exc import SQLAlchemyError


#  ---------------------IMPORTING MIDDLEWARE----------------
from middleware.logging_middleware import (
    LoggingMiddleware
    
    
)
#---------------------FASTAPI APP CREATE----------------
app = FastAPI(

    title="Expense Tracker API",

    description="""
    Expense Tracker API with JWT Authentication
    """,

    version="1.0.0",

    docs_url="/docs",

    redoc_url="/redoc"
)

#---------------------AAPPLY CORS MIDDLEWARE----------------
add_cors(app)


#---------------------REGISTER ROUTER----------------
app.include_router(expense_router)

app.include_router(put_del_router)

app.include_router(auth_router)

app.include_router(dashboard_router)

# ---------------------CREATE TABLE IN DATABASE----------------




# ---------------------GOABL EXCEPTION HANDLER---------------------
 
# -------- REGISTER EXCEPTION HANDLERS --------

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    SQLAlchemyError,
    database_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

# ---------------------REGISTER MIDDLEWARE----------------
app.add_middleware(
    LoggingMiddleware
)