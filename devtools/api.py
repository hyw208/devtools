from fastapi import FastAPI
import os
from devtools.utils.logging import getLogging as logging
logger = logging()
from dotenv.main import load_dotenv
load_dotenv()
from pydantic import BaseModel
from celery.result import AsyncResult
import names
import random
from devtools.tasks import sample
from devtools.app import app as celery_app

class TaskOut(BaseModel):
    id: str
    status: str

def app():
    api = FastAPI()

    @api.get("/hello")
    async def hello() -> dict:
        return {"message": "Hello World DevTools!"}

    @api.get("/start")
    async def start() -> TaskOut:
        # res = sample.sample_task.delay(names.get_full_name())
        # return TaskOut(id=res.task_id, status=res.status)
        res = celery_app.send_task('sample', args=[names.get_full_name()], queue=random.choice(['xxx', 'yyy']))
        return TaskOut(id=res.task_id, status=res.status)

    @api.get("/status")
    async def status(task_id: str) -> TaskOut:
        # res = sample.app.AsyncResult(task_id)
        # return TaskOut(id=res.task_id, status=res.status)
        res = celery_app.AsyncResult(task_id)
        return TaskOut(id=res.task_id, status=res.status)

    return api


def main():
    import uvicorn

    API_PORT = os.getenv("API_PORT", "8080")
    logger.info(f"DevTools api port is {API_PORT}")

    uvicorn.run(app(), host="0.0.0.0", port=int(API_PORT))
    

if __name__ == "__main__":
    main()