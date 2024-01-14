#!/usr/bin/env python3
# coding=utf-8
# date 2024-01-13 06:59:57
# author calllivecn <c-all@qq.com>

import uvicorn

headers = [
    ("Server", "nginx"),
]

uvicorn.run("01-fastapi:app", host="10.1.3.1", port=8000, headers=headers, log_level="info") # , reload=True) # 怎么报错？。。。
#uvicorn.run("01-fastapi:app", host="10.1.3.1", port=8000, headers=headers, log_level="warning")

