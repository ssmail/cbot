# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
from dataclasses import dataclass

import click
import requests
from sqlalchemy.ext.declarative import declarative_base

from mantis import db

from mantis.models import *


def init_db():
    click.echo('Initialized the database')
    # from mantis.models.token import Token
    # from mantis.models.user import User
    # from mantis.models.slack import Slack

    Base = declarative_base()
    db.create_all()


@click.command()
def init():
    click.echo('Initialized the database')
    init_db()


@dataclass
class SlackUser:
    workspace: str
    username: str
    password: str
    description: str
    token: str
    cookie: str


account_level_enable_pmi = SlackUser(
    workspace="carterbot",
    username="carter.hong@zoomus.ltd",
    password="Slack.123456",
    description="Admin账号",
    token="",
    cookie=""
)


def init_user(user):
    resp = requests.post("https://devslackbot.zoomdev.us/api/account/add", data={
        "username": user.username,
        "password": user.password,
        "workspace": user.workspace,
        "token": user.token,
        "cookie": user.cookie
    })

    print(resp.text)


if __name__ == '__main__':
    init_db()
    init_user(account_level_enable_pmi)
