# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong

from dataclasses import dataclass

import click
import requests
from sqlalchemy.ext.declarative import declarative_base

from mantis import db

from mantis.models import *


@dataclass
class SlackUser:
    workspace: str
    username: str
    password: str
    description: str = ""
    token: str = ""
    cookie: str = ""


def init_db():
    click.echo('Initialized the database')

    Base = declarative_base()
    db.create_all()


@click.command()
def init():
    click.echo('Initialized the database')
    init_db()


class SlackUserList:
    a1 = SlackUser(
        workspace="carterbot",
        username="carter.hong@zoomus.ltd",
        password="Slack.123456",
        description="Admin账号",
        token="",
        cookie=""
    )

    a2 = SlackUser(
        workspace="carterbot",
        username="carter.hong_a1@zoomus.ltd",
        password="Slack.123456",
        description="Admin账号",
        token="",
        cookie=""
    )

    a3 = SlackUser(
        workspace="hongweb",
        username="carter.hong_a1@zoomus.ltd",
        password="Slack.123456",
        description="Admin账号",
        token="",
        cookie=""
    )
    a4 = SlackUser(
        workspace="carterbot",
        username="carter.hong_cn@cn.zoomus.ltd",
        password="Slack.123456",
        description="cn用户",
        token="",
        cookie=""
    )


def init_user(slack: SlackUser):
    resp = requests.post(SERVER_ADDRESS, data=slack.__dict__)
    print(resp.text)


# SERVER_ADDRESS = "http://localhost:8000/account/add"
SERVER_ADDRESS = "https://devslackbot.zoomdev.us/api/account/add"

if __name__ == '__main__':
    # init_db()
    # init_user(account_level_enable_pmi)
    for _ in SlackUserList.__dict__.keys():
        if not _.startswith("__"):
            user: SlackUser = SlackUserList.__dict__.get(_)
            init_user(user)
