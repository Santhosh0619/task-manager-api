from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse
from app.core.security import get_current_user
from app.models.user import User
from app.core.logger import logger


router = APIRouter()


@router.post("/tasks", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info(f"Task created by user {current_user.id}: {new_task.title}")

    return new_task


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()

    logger.info(f"User {current_user.id} fetched their tasks")

    return tasks


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        logger.error(f"Unauthorized update attempt by user {current_user.id} on task {task_id}")
        return {"error": "Task not found or not authorized"}

    task.title = updated_task.title
    task.description = updated_task.description
    task.status = updated_task.status
    task.priority = updated_task.priority

    db.commit()
    db.refresh(task)

    logger.info(f"Task {task_id} updated by user {current_user.id}")

    return task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        logger.error(f"Unauthorized delete attempt by user {current_user.id} on task {task_id}")
        return {"error": "Task not found or not authorized"}

    db.delete(task)
    db.commit()

    logger.warning(f"Task {task_id} deleted by user {current_user.id}")

    return {"message": "Task deleted successfully"}