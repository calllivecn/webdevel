#!/usr/bin/env python3
# coding=utf-8
# date 2024-01-13 07:16:49
# author calllivecn <c-all@qq.com>


import subprocess


subprocess.run(["uwsgi", "--ini", "uwsgi.ini"])
#subprocess.run(["uwsgi", "--ini", "uWSGI-django.ini"])

