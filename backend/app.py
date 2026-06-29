from flask import Flask, request, jsonify

from db import init_db, SessionLocal
from models import Robot
from services import task_service

app = Flask(__name__)


@app.route("/tasks", methods=["POST"])
def create_task():
    db = SessionLocal()
    response, status_code = task_service.create_task(db, request.get_json())
    db.close()
    return jsonify(response), status_code


@app.route("/tasks", methods=["GET"])
def get_tasks():
    db = SessionLocal()
    response, status_code = task_service.get_tasks(db)
    db.close()
    return jsonify(response), status_code


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    db = SessionLocal()
    response, status_code = task_service.get_task(db, task_id)
    db.close()
    return jsonify(response), status_code


@app.route("/robots", methods=["GET"])
def get_robots():
    db = SessionLocal()
    response, status_code = task_service.get_robots(db)
    db.close()
    return jsonify(response), status_code


def seed_robots():
    db = SessionLocal()

    if db.query(Robot).count() == 0:
        db.add(Robot(id="robot_1", status="IDLE"))
        db.add(Robot(id="robot_2", status="IDLE"))
        db.commit()

    db.close()


if __name__ == "__main__":
    init_db()
    seed_robots()
    app.run(debug=True, port=5000)