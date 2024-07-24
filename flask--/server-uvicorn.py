#!/usr/bin/env python3
# coding=utf-8
# date 2024-04-23 23:27:52
# author calllivecn <calllivecn@outlook.com>

# flask + uvicorn 可以的，需要使用 asgiref

import uvicorn

headers = [
    ("Server", "nginx"),
]

#uvicorn.run("flask-01:app", host="::", port=8000, headers=headers, log_level="info") # , reload=True) # 怎么报错？。。。
uvicorn.run("flask-01:asgi_app", host="::", port=8000, headers=headers, log_level="info")

