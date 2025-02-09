# app/routes/task_routes.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import redis
import json
from datetime import datetime
from pydantic import BaseModel
from app.config import REDIS_HOST
from app.tasks import update_task_to_active, update_task_to_completed

router = APIRouter()

# Initialize Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


class TaskRequest(BaseModel):
    task: str
    start_time: str  # Format: "HH:MM AM/PM"
    end_time: str  # Format: "HH:MM AM/PM"


@router.post("/schedule_task")
async def schedule_task(task_req: TaskRequest):
    task_name = task_req.task
    start_time_str = task_req.start_time
    end_time_str = task_req.end_time

    if not (task_name and start_time_str and end_time_str):
        raise HTTPException(
            status_code=400, detail="Please provide task, start_time, and end_time."
        )

    try:
        # Convert input times to 24-hour format (HH:MM)
        start_time_formatted = datetime.strptime(start_time_str, "%I:%M %p").strftime(
            "%H:%M"
        )
        end_time_formatted = datetime.strptime(end_time_str, "%I:%M %p").strftime(
            "%H:%M"
        )
        if end_time_formatted <= start_time_formatted:
            raise HTTPException(
                status_code=400, detail="End time must be after start time"
            )
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid time format. Use 'HH:MM AM/PM'"
        )

    # Prevent duplicate scheduling for the same time
    existing_tasks = redis_client.hgetall("tasks")
    for t in existing_tasks.values():
        task_info = json.loads(t)
        if (
            task_info["start_time"] == start_time_formatted
            and task_info["end_time"] == end_time_formatted
        ):
            raise HTTPException(
                status_code=400, detail="A task is already scheduled for this time"
            )

    # Generate a unique task ID
    task_id = redis_client.incr("task_id")

    now = datetime.now()
    current_time = now.strftime("%H:%M")
    if current_time >= end_time_formatted:
        status = "Completed"
    elif start_time_formatted <= current_time < end_time_formatted:
        status = "Active"
    else:
        status = "Pending"

    # Save task in Redis
    task_data = {
        "task_id": task_id,
        "task_name": task_name,
        "start_time": start_time_formatted,
        "end_time": end_time_formatted,
        "status": status,
    }
    redis_client.hset("tasks", task_id, json.dumps(task_data))

    # Calculate datetime objects for today based on start/end times
    start_dt = datetime.strptime(start_time_formatted, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )
    end_dt = datetime.strptime(end_time_formatted, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )

    # Schedule Celery tasks using ETA if the scheduled time is in the future
    if now < start_dt:
        update_task_to_active.apply_async(args=[task_id], eta=start_dt)
    else:
        update_task_to_active.delay(task_id)

    if now < end_dt:
        update_task_to_completed.apply_async(args=[task_id], eta=end_dt)
    else:
        update_task_to_completed.delay(task_id)

    return JSONResponse(
        content={"message": "Task scheduled", "task_id": task_id, "status": status}
    )


@router.get("/tasks")
async def get_all_tasks():
    tasks = redis_client.hgetall("tasks")
    task_list = [json.loads(t) for t in tasks.values()]
    return JSONResponse(content=task_list)


@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = redis_client.hget("tasks", task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return JSONResponse(content=json.loads(task))


@router.get("/active_task")
async def get_active_task():
    current_time = datetime.now().strftime("%H:%M")
    tasks = redis_client.hgetall("tasks")
    for t in tasks.values():
        task_info = json.loads(t)
        if task_info["start_time"] <= current_time < task_info["end_time"]:
            return JSONResponse(content=task_info)
    return JSONResponse(content={"message": "No active tasks"}, status_code=200)
