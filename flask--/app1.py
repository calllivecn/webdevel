#!/usr/bin/env python3
# coding=utf-8
# date 2024-02-03 02:41:07
# author calllivecn <c-all@qq.com>


from asgiref.wsgi import WsgiToAsgi
from flask import Flask

app = Flask(__name__)

@app.route("/")
async def index():
    return "<p>Hello, World!</p>"

app = WsgiToAsgi(app)

