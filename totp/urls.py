#!/usr/bin/env python3
# coding=utf-8
# date 2024-01-13 03:38:45
# author calllivecn <c-all@qq.com>

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]

