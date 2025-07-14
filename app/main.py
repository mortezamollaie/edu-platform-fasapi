from fastapi import FastAPI
from app.api.api_v1 import user
from app.db.init_db import init_db

app = FastAPI(title="Edu Platform")

# include routers
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])

# create tables on startup
@app.on_event("startup")
def on_startup():
    init_db()