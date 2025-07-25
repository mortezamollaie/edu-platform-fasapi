from fastapi import FastAPI
from app.api.api_v1 import courses, user, account, chapters, lectures, roles, permissions
from app.db.init_db import init_db
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="Edu Platform")

app.add_middleware(SessionMiddleware, secret_key="YOUR_SECRET_KEY_HERE")

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(account.router, prefix="/api/v1/accounts", tags=["Accounts"])
app.include_router(courses.router, prefix="/api/v1", tags=["Courses"])
app.include_router(chapters.router, prefix="/api/v1", tags=["Chapters"])
app.include_router(lectures.router, prefix="/api/v1", tags=["Lectures"])
app.include_router(roles.router, prefix="/api/v1/roles", tags=["Roles"])
app.include_router(permissions.router, prefix="/api/v1/permissions", tags=["Permissions"])

@app.on_event("startup")
def on_startup():
    init_db()