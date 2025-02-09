from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.task_routes import router as task_router

app = FastAPI(
    title="Task Scheduler API",
    description=(
        "This API provides task scheduling functionalities, allowing users "
        "to schedule tasks for execution at specific times. The system uses "
        "a queue (RabbitMQ) to process tasks asynchronously and stores task "
        "details in Redis. \n\n"
        "**Key Features:**\n"
        "- Schedule tasks with a start and end time\n"
        "- Retrieve all scheduled tasks\n"
        "- Fetch a specific task by ID\n"
        "- Check currently active tasks\n\n"
        "**Time Handling:**\n"
        "- The API follows UTC (Coordinated Universal Time) internally for all task scheduling, "
        "timestamps, and time-based calculations."
    ),
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your-email@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Enable CORS (Cross-Origin Resource Sharing) for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to a specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(task_router, prefix="/api/v1", tags=["Task Management"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)
