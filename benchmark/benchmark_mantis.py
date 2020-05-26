# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
from locust import HttpLocust, TaskSet


def login(l):
    l.client.post("/user/login", {"username": "admin", "password": "123456"})


def logout(l):
    l.client.post("/user/logout", {"username": "ellen_key", "password": "education"})


def index(l):
    l.client.get("/")


def profile(l):
    l.client.get("/profile")


class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
