from fastapi import FastAPI

#---------------------IMPORTING MIDDLEWARE-----------------
from middleware.cors import add_cors


from Routes.expenses  import router as expense_router

from Routes.put_del_exp import router as put_del_router

# ---------------------IMPORTING DATABASE----------------
from database.connection import engine , Base


#---------------------FASTAPI APP CREATE----------------
app = FastAPI(
     title="Expense Tracker API",
    version="1.0.0"
)

#---------------------AAPPLY CORS MIDDLEWARE----------------
add_cors(app)


#---------------------INCLUDE ROUTER----------------
app.include_router(expense_router)

app.include_router(put_del_router)


# ---------------------CREATE TABLE IN DATABASE----------------
Base.metadata.create_all(bind=engine)