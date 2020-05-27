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


@dataclass
class ZoomMessage:
    workspace: str
    userId: str
    channel: str
    title: str
    meetingId: str
    messageType: str
    subtype: str
    password: str
    text: str
    dateStart: str
    botId: str
    createBy: str
