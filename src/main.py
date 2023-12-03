import uvicorn
from fastapi import FastAPI
from api import health, user, expense, balance
from db import models
from db.postgre import engine

# creates table in databse
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(health.router)
app.include_router(user.router)
app.include_router(expense.router)
app.include_router(balance.router)

if __name__ == "__main__":
    uvicorn.run(app=app)
