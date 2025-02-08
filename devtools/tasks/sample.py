from devtools.app import app
import time
import random
from devtools.utils.logging import getLogging as logging
logger = logging()

@app.task(name='sample')
def sample_task(name):
    _sec = random.randint(5, 60)
    logger.info(f"{name} to sleep for {_sec} seconds")
    time.sleep(_sec)
    logger.info(f"{name} just woke up!")

    return {'name': name, 'seconds': _sec}