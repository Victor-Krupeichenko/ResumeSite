import os
from celery import Celery
from dotenv import load_dotenv
load_dotenv()

broker_and_backend = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}"

app_celery = Celery(
    main="tasks",
    broker=broker_and_backend,
    backend=broker_and_backend,
    broker_connection_retry_on_startup=True,  # Отключает предупреждение
)
