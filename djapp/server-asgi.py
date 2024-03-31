#!/usr/bin/env python3
# coding=utf-8
# date 2024-01-13 06:59:57
# author calllivecn <calllivecn@outlook.com>

import uvicorn

headers = [
    ("Server", "nginx"),
]

#uvicorn.run("djapp.asgi:application", host="10.1.3.1", port=8001, log_level="info")
uvicorn.run("djapp.asgi:application", host="10.1.3.1", port=8001, headers=headers, log_level="info") # , reload=True) # 怎么报错？。。。

