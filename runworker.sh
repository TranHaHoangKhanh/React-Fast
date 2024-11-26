celery -A src.utils.celery_tasks.c_app worker --loglevel=INFO &

celery -A src.utils.celery_tasks.c_app flower