from repositories import task_repository


def task_to_dict(task):
    return {
        "id": task.id,
        "pickup_location": task.pickup_location,
        "dropoff_location": task.dropoff_location,
        "priority": task.priority,
        "status": task.status,
        "assigned_robot_id": task.assigned_robot_id,
        "retry_count": task.retry_count,
    }


def robot_to_dict(robot):
    return {
        "id": robot.id,
        "status": robot.status,
        "current_task_id": robot.current_task_id,
    }


def create_task(db, data):
    if not data:
        return {"error": "Request body is required"}, 400

    pickup = data.get("pickup_location")
    dropoff = data.get("dropoff_location")
    priority = data.get("priority", "normal")

    if not pickup or not dropoff:
        return {"error": "pickup_location and dropoff_location are required"}, 400

    task = task_repository.create_task(db, pickup, dropoff, priority)
    return task_to_dict(task), 201


def get_tasks(db):
    tasks = task_repository.get_all_tasks(db)
    return [task_to_dict(task) for task in tasks], 200


def get_task(db, task_id):
    task = task_repository.get_task_by_id(db, task_id)

    if not task:
        return {"error": "Task not found"}, 404

    return task_to_dict(task), 200


def get_robots(db):
    robots = task_repository.get_all_robots(db)
    return [robot_to_dict(robot) for robot in robots], 200