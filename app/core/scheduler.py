from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.task import Task


def check_pending_tasks():
    db: Session = SessionLocal()

    try:
        pending_tasks = db.query(Task).filter(Task.status == "pending").all()

        if pending_tasks:
            print("🔔 Pending Tasks Reminder:")
            for task in pending_tasks:
                print(f"User {task.user_id} has pending task: {task.title}")
        else:
            print("✅ No pending tasks")

    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(check_pending_tasks, "interval", minutes=1)  # change later to daily
scheduler.start()