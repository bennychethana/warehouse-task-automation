import json

import paho.mqtt.client as mqtt


BROKER = "localhost"
PORT = 1883
TASK_TOPIC = "tasks/assigned"


def publish_task(robot_id, task):
    client = mqtt.Client()
    client.connect(BROKER, PORT)

    payload = {
        "task_id": task.id,
        "robot_id": robot_id,
        "pickup_location": task.pickup_location,
        "dropoff_location": task.dropoff_location,
        "priority": task.priority,
    }

    client.publish(TASK_TOPIC, json.dumps(payload))
    client.disconnect()