from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from app.db.database import Base
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__="tasks"

    id=Column(Integer, primary_key=True, index=True)
    title=Column(String(200))
    description=Column(String(500))
    status=Column(Enum("pending", "completed"), default="pending")
    priority=Column(Enum("low", "medium", "high"), default="low")

    user_id=Column(Integer, ForeignKey("users.id"))

    user=relationship("User")


