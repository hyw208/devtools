import random
import time

from celery import Task
from devtools.app import app
from devtools.utils.logging import getLogging as logging

logger = logging()

class BaseTaskWithRetry(Task):
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print(f"Retrying task {task_id} due to {exc}...")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f"Task {task_id} failed after retries: {exc}")

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

@app.task(name='add', bind=True)
def add(self, x, y):
    _sec = random.randint(5, 60)
    logger.info(f"add({x}, {y}) is about to sleep {_sec} seconds")
    time.sleep(_sec)
    ans = x + y
    logger.info(f"add({x}, {y}) = {ans}")
    return ans

@app.task(name='multiply', bind=True)
def multiply(self, x, y):
    _sec = random.randint(5, 60)
    logger.info(f"multiply({x}, {y}) is about to sleep {_sec} seconds")
    time.sleep(_sec)
    ans = x * y
    logger.info(f"multiply({x}, {y}) = {ans}")
    return ans 

@app.task(name='subtract', bind=True)
def subtract(self, x, y):
    _sec = random.randint(5, 60)
    logger.info(f"subtract({x}, {y}) is about to sleep {_sec} seconds")
    time.sleep(_sec)
    ans = x - y
    logger.info(f"subtract({x}, {y}) = {ans}")
    return ans 