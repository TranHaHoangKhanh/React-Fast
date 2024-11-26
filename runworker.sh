celery -A src.utils.celery_tasks.c_app work --loglevel=INFO &

celery -A src.utils.celery_tasks.c_app flower