#!/usr/bin/env python3
# coding=utf-8
# date 2024-01-13 06:59:57
# author calllivecn <c-all@qq.com>

import os

import uvicorn

headers = [
    ("Server", "nginx"),
]

app_main = "01-fastapi:app"

import multiprocessing.util

if __name__ == "__main__":
    multiprocessing.freeze_support()

    #uvicorn.run(app_main, host="10.1.3.1", port=8000, headers=headers, workers=os.cpu_count(), log_level="info") # , reload=True) # 怎么报错？。。。
    uvicorn.run(app_main, host="10.1.3.1", port=8000, headers=headers, workers=os.cpu_count(), log_level="warning")

