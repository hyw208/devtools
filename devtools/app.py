from celery.app import Celery
import os
from devtools.utils.logging import getLogging as logging
logger = logging()
from dotenv.main import load_dotenv
load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://0.0.0.0:6379")
logger.info(f"DevTools redis url {redis_url}")

app = Celery("devtools-celery", broker=redis_url, backend=redis_url)

app.conf.update(enable_utc=True, timezone='Europe/London')