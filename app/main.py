from fastapi import FastAPI
from app.api.api_v1 import user, account
from app.db.init_db import init_db
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(title="Edu Platform")

# include routers
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(account.router, prefix="/api/v1/accounts", tags=["Accounts"])

# create tables on startup
@app.on_event("startup")
def on_startup():
    init_db()