from db import reset_db, SessionLocal
from models import Robot

reset_db()

db = SessionLocal()

db.add(Robot(id="robot_1", status="IDLE"))
db.add(Robot(id="robot_2", status="IDLE"))

db.commit()
db.close()

print("Database reset successfully.")