from app.db.database import SessionLocal
from app.models.task import Task

db = SessionLocal()

BATCH_SIZE = 1000

offset = 0

while True:
    tasks = db.query(Task).offset(offset).limit(BATCH_SIZE).all()

    if not tasks:
        break

    for task in tasks:
        if task.status == "pending":
            task.status_new = 0
        elif task.status == "completed":
            task.status_new = 1

        if task.priority == "low":
            task.priority_new = 1
        elif task.priority == "medium":
            task.priority_new = 2
        elif task.priority == "high":
            task.priority_new = 3

    db.commit()
    offset += BATCH_SIZE

db.close()