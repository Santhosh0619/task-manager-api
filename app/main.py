from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import user, task
from app.api import user, task
from app.core import scheduler

app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(task.router)

