#!/usr/bin/env python3
# coding=utf-8
# date 2024-01-13 03:38:45
# author calllivecn <calllivecn@outlook.com>

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("a/", views.index, name="aindex"),
    path("json/", views.json),
    path("404/", views.err404),
    path("500/", views.err500),

]

