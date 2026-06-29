import time

from db import SessionLocal
from repositories import task_repository
from mqtt.publisher import publish_task

MAX_RETRIES = 3

def republish_stale_tasks(db):
    stale_tasks = task_repository.get_stale_assigned_tasks(db, timeout_seconds=10)

    for task in stale_tasks:
        if task.retry_count >= MAX_RETRIES:
            task.status = "FAILED"
            db.commit()
            print(f"Task {task.id} failed after max retries.")
            continue

        task_repository.increment_retry_count(db, task)
        publish_task(task.assigned_robot_id, task)
        print(f"Republished task {task.id} to {task.assigned_robot_id}. Retry {task.retry_count}")


def scheduler_loop():

    while True:

        db = SessionLocal()

        task = task_repository.get_oldest_pending_task(db)
        robot = task_repository.get_idle_robot(db)

        if task is None:
            print("No pending tasks.")

        elif robot is None:
            print("No idle robots.")

        else:
            task_repository.assign_task(db, task, robot)

            publish_task(robot.id, task)

            print(f"Published Task {task.id} to {robot.id}")

        republish_stale_tasks(db)

        db.close()

        time.sleep(2)


if __name__ == "__main__":
    scheduler_loop()