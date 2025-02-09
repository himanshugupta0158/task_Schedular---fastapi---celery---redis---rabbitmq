# Project Overview
This project allows you to schedule tasks for the current day by specifying a start time and end time. Tasks are stored in Redis, and their status is updated automatically by Celery tasks. The statuses cycle from Pending → Active → Completed based on the specified time window.

- FastAPI handles incoming HTTP requests.
- RabbitMQ is used as the broker for Celery’s background task processing.
- Celery schedules status updates at the exact times you specify.
- Redis stores task information (e.g., start/end times, status, name).

<hr>

## Architecture

                   +-----------------------+
                   |      FastAPI App     |
                   | (fastapi_app service)|
                   +----------+-----------+
                              |
                              | REST API
                              |
                              v
                        [ User Client ]
                              ^
                              |
                              |
                   +----------+-----------+
                   |      Celery Worker  |
                   | (celery_worker svc) |
                   +----------+-----------+
                              |
                           RabbitMQ
                              |
                              v
                           [Broker]
                              ^
                              |
                   +----------+-----------+
                   |        Redis        |
                   |   (Key-Value Store) |
                   +----------------------+

1. User sends an HTTP request to the FastAPI app to schedule or retrieve tasks.
2. FastAPI saves task info in Redis and also sends messages to the Celery Worker via RabbitMQ.
3. Celery Worker receives tasks at the specified times and updates statuses in Redis accordingly.

## Features
- Schedule a Task: Provide a task name, start time, and end time for the current day.
- Automatic Status Updates: Status changes to Active at start_time and Completed at end_time.
- Collision Detection: Prevent scheduling a second task in the exact same time window.
- View Scheduled Tasks: Retrieve all tasks or a single task by ID.
- Check Active Task: Query which task (if any) is currently active.


## Prerequisites
- Docker: Make sure Docker Engine is installed and running.
- Docker Compose: Ensure Docker Compose is installed (comes with Docker Desktop on Windows/macOS; separate package on Linux).


### Steps to Follow
1. Clone repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Build and start the containers:
```bash
docker-compose up --build
```

3. stop docker container : CTRL + C and use below code in terminal
```bash
docker-compose down
```