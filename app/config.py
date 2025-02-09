# app/config.py
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")
