# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong
from dataclasses import dataclass


@dataclass
class SlackUser:
    workspace: str
    username: str
    password: str
    description: str
    pmi: str


@dataclass
class AuthenticatedSlackUser:
    workspace: str
    username: str
    password: str
    token: str
    cookie: str
    description: str
    pmi: str


class SlackWorkSpace:
    carterbot = "carterbot"
    hongweb = "hongweb"
