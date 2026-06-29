from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    pickup_location = Column(String, nullable=False)
    dropoff_location = Column(String, nullable=False)
    priority = Column(String, nullable=False, default="normal")
    status = Column(String, nullable=False, default="PENDING")
    assigned_robot_id = Column(String, nullable=True)
    retry_count = Column(Integer, nullable=False, default=0)
    assigned_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class Robot(Base):
    __tablename__ = "robots"

    id = Column(String, primary_key=True)
    status = Column(String, nullable=False, default="IDLE")
    current_task_id = Column(Integer, nullable=True)