import json

import paho.mqtt.client as mqtt

from db import SessionLocal
from repositories import task_repository


BROKER = "localhost"
PORT = 1883
STATUS_TOPIC = "robots/status"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Status listener connected to MQTT broker.")
        client.subscribe(STATUS_TOPIC)
        print(f"Subscribed to {STATUS_TOPIC}")
    else:
        print(f"Failed to connect. Return code: {rc}")


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())

    task_id = payload["task_id"]
    robot_id = payload["robot_id"]
    status = payload["status"]

    db = SessionLocal()

    try:
        if status == "TASK_RECEIVED":
            task_repository.update_task_status(db, task_id, "IN_PROGRESS")
            print(f"Task {task_id} is now IN_PROGRESS.")

        elif status == "COMPLETED":
            task_repository.update_task_status(db, task_id, "COMPLETED")
            task_repository.mark_robot_idle(db, robot_id)
            print(f"Task {task_id} completed by {robot_id}. Robot is now IDLE.")

        elif status == "FAILED":
            task_repository.update_task_status(db, task_id, "FAILED")
            task_repository.mark_robot_idle(db, robot_id)
            print(f"Task {task_id} failed on {robot_id}. Robot is now IDLE.")

        else:
            print(f"Unknown status received: {status}")

    finally:
        db.close()


def main():
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT)
    client.loop_forever()


if __name__ == "__main__":
    main()