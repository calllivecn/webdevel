from typing import Annotated

import time

from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI(
    title="自测系统",
    description="这是描述",
    summary="人类精神状态自我测试系统",
    version="0.1",
)


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        time.sleep(5)
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}