from devtools.app import app
from celery import Task
import time
import random
from devtools.utils.logging import getLogging as logging
logger = logging()

@app.task(name='sample', 
    bind=True, 
    max_retries=5,
    default_retry_delay=3,
    soft_time_limit=30)
def sample_task(self, name):
    try: 
        _sec = random.randint(5, 60)
        logger.info(f"{name} to sleep for {_sec} seconds")
        time.sleep(_sec)
        logger.info(f"{name} just woke up!")
        res = {'name': name, 'seconds': _sec}
    except Exception as ex:
        self.retry(exc=ex)

    return res


class BaseTaskWithRetry(Task):
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print(f"Retrying task {task_id} due to {exc}...")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f"Task {task_id} failed after retries: {exc}")


@app.task(name='sample2', 
    bind=True, 
    base=BaseTaskWithRetry,
    max_retries=5,
    default_retry_delay=3,
    soft_time_limit=10)
def sample2_task(self, name):
    try: 
        _sec = random.randint(5, 60)
        logger.info(f"{name} to sleep for {_sec} seconds")
        time.sleep(_sec)
        logger.info(f"{name} just woke up!")
        res = {'name': name, 'seconds': _sec}
    except Exception as ex:
        self.retry(exc=ex)

    return res