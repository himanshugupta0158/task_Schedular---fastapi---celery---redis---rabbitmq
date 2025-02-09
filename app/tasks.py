# app/tasks.py
import json
import redis
from app.config import REDIS_HOST
from app.celery_app import celery_app  # Use the renamed Celery app

# Initialize Redis client (ensure decode_responses=True)
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


@celery_app.task
def update_task_to_active(task_id):
    """
    Celery task to update a scheduled task's status to Active.
    """
    task_data = redis_client.hget("tasks", task_id)
    if not task_data:
        print(f"[Active] No task found with id {task_id}.")
        return
    task = json.loads(task_data)
    if task.get("status") != "Active":
        task["status"] = "Active"
        redis_client.hset("tasks", task_id, json.dumps(task))
        print(f"[Active] Task {task_id} ('{task.get('task_name')}') updated to Active.")
    else:
        print(f"[Active] Task {task_id} already Active.")


@celery_app.task
def update_task_to_completed(task_id):
    """
    Celery task to update a scheduled task's status to Completed.
    """
    task_data = redis_client.hget("tasks", task_id)
    if not task_data:
        print(f"[Completed] No task found with id {task_id}.")
        return
    task = json.loads(task_data)
    if task.get("status") != "Completed":
        task["status"] = "Completed"
        redis_client.hset("tasks", task_id, json.dumps(task))
        print(
            f"[Completed] Task {task_id} ('{task.get('task_name')}') updated to Completed."
        )
    else:
        print(f"[Completed] Task {task_id} already Completed.")
