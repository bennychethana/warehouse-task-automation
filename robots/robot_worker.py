import json
import sys
import time

import paho.mqtt.client as mqtt


BROKER = "localhost"
PORT = 1883

ROBOT_ID = sys.argv[1] if len(sys.argv) > 1 else "robot_1"

TASK_TOPIC = "tasks/assigned"
STATUS_TOPIC = "robots/status"


def publish_status(client, task_id, status):
    payload = {
        "task_id": task_id,
        "robot_id": ROBOT_ID,
        "status": status,
    }

    client.publish(STATUS_TOPIC, json.dumps(payload))
    print(f"Published status: {payload}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"{ROBOT_ID} connected to MQTT broker.")
        client.subscribe(TASK_TOPIC)
        print(f"{ROBOT_ID} subscribed to {TASK_TOPIC}")
    else:
        print(f"Failed to connect. Return code: {rc}")


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())

    if payload.get("robot_id") != ROBOT_ID:
        return

    task_id = payload["task_id"]
    pickup = payload["pickup_location"]
    dropoff = payload["dropoff_location"]

    print(f"{ROBOT_ID} received task {task_id}: {pickup} -> {dropoff}")

    publish_status(client, task_id, "TASK_RECEIVED")

    print(f"{ROBOT_ID} moving from {pickup} to {dropoff}...")
    time.sleep(5)

    publish_status(client, task_id, "COMPLETED")

    print(f"{ROBOT_ID} completed task {task_id}")


def main():
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT)
    client.loop_forever()


if __name__ == "__main__":
    main()