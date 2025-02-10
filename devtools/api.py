import os
import random

import names
from celery import group, signature
from celery.result import AsyncResult, GroupResult
from dotenv.main import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from devtools.app import app as celery_app
from devtools.utils.logging import getLogging as logging

logger = logging()
load_dotenv()


class TaskOut(BaseModel):
    id: str
    ready: bool
    result: object = None

def app():
    api = FastAPI()

    @api.get("/hello")
    async def hello() -> dict:
        return {"message": "Hello World DevTools!"}

    @api.get("/sample1")
    async def sample1() -> TaskOut:
        # res = sample.sample_task.delay(names.get_full_name())
        # return TaskOut(id=res.task_id, status=res.status)
        res = celery_app.send_task('sample', args=[names.get_full_name()], queue=random.choice(['xxx', 'yyy']))
        return TaskOut(id=res.task_id, ready=res.ready())
    
    @api.get("/sample2")
    async def sample2() -> TaskOut:
        # res = sample.sample_task.delay(names.get_full_name())
        # return TaskOut(id=res.task_id, status=res.status)
        res = celery_app.send_task('sample2', args=[names.get_full_name()], queue='xxx')
        return TaskOut(id=res.task_id, ready=res.ready())

    @api.get("/status")
    async def status(id: str) -> TaskOut:
        # res = sample.app.AsyncResult(task_id)
        # return TaskOut(id=res.task_id, status=res.status)
        
        # id could be AsyncResult task id or GroupResult id
        try:
            res = GroupResult.restore(id)
            if res and isinstance(res, GroupResult):    
                # GroupResult
                logger.info("#### res is GroupResult")
                return TaskOut(id=res.id, ready=res.ready(), result=res.get() if res.ready() else None)
            else:
                # AsyncResult (single task)
                logger.info("#### res is AsyncResult")
                res = AsyncResult(id)
                return TaskOut(id=res.id, ready=res.ready(), result=res.get() if res.ready() else None)
        
        except (ValueError, TypeError) as ex:
            return TaskOut(id=id, status="Invalid", result=str(ex))

    @api.get("/grouping")
    async def grouping() -> TaskOut:
        add_ = signature('add', args=(1, 3), immutable=True, debug=True).set(queue=random.choice(['xxx', 'yyy']))
        multiply_ = signature('multiply', immutable=True, args=(2, 2), debug=True).set(queue=random.choice(['xxx', 'yyy']))
        subtract_ = signature('subtract', immutable=True, args=(6, 2), debug=True).set(queue=random.choice(['xxx', 'yyy']))
        res = group([add_, multiply_, subtract_]).apply_async()
        res.save() # have to save before it can be restored later
        return TaskOut(id=res.id, ready=res.ready())

    return api


def main():
    import uvicorn

    API_PORT = os.getenv("API_PORT", "8080")
    logger.info(f"DevTools api port is {API_PORT}")

    uvicorn.run(app(), host="0.0.0.0", port=int(API_PORT))
    

if __name__ == "__main__":
    main()