#!/usr/bin/env python3
# coding=utf-8
# date 2024-01-13 06:59:57
# author calllivecn <c-all@qq.com>

import uvicorn

#uvicorn.run("djapp.asgi:application", host="10.1.3.1", port=8000, log_level="info")
uvicorn.run("djapp.asgi:application", host="10.1.3.1", port=8000, log_level="warning")

