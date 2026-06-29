from models import Task, Robot

from datetime import datetime, timezone, timedelta


def create_task(db, pickup_location, dropoff_location, priority):
    task = Task(
        pickup_location=pickup_location,
        dropoff_location=dropoff_location,
        priority=priority,
        status="PENDING",
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_all_tasks(db):
    return db.query(Task).all()


def get_task_by_id(db, task_id):
    return db.query(Task).filter(Task.id == task_id).first()


def get_all_robots(db):
    return db.query(Robot).all()

def get_oldest_pending_task(db):
    return (
        db.query(Task)
        .filter(Task.status == "PENDING")
        .order_by(Task.created_at)
        .first()
    )


def get_idle_robot(db):
    return (
        db.query(Robot)
        .filter(Robot.status == "IDLE")
        .first()
    )


def assign_task(db, task, robot):
    task.status = "ASSIGNED"
    task.assigned_robot_id = robot.id
    task.assigned_at = datetime.now(timezone.utc)

    robot.status = "BUSY"
    robot.current_task_id = task.id

    db.commit()

def update_task_status(db, task_id, status):
    task = get_task_by_id(db, task_id)

    if task:
        task.status = status
        db.commit()


def get_robot_by_id(db, robot_id):
    return db.query(Robot).filter(Robot.id == robot_id).first()


def mark_robot_idle(db, robot_id):
    robot = get_robot_by_id(db, robot_id)

    if robot:
        robot.status = "IDLE"
        robot.current_task_id = None
        db.commit()

def get_stale_assigned_tasks(db, timeout_seconds=10):
    cutoff = datetime.now(timezone.utc) - timedelta(seconds=timeout_seconds)

    return (
        db.query(Task)
        .filter(Task.status == "ASSIGNED")
        .filter(Task.assigned_at < cutoff)
        .all()
    )


def increment_retry_count(db, task):
    task.retry_count += 1
    task.assigned_at = datetime.now(timezone.utc)
    db.commit()