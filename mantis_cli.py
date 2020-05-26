# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
import click
from sqlalchemy.ext.declarative import declarative_base

from mantis import db


def init_db():
    from mantis.models.token import Token
    from mantis.models.user import User
    from mantis.models.slack import Slack
    Base = declarative_base()
    db.create_all()


@click.command()
def init():
    click.echo('Initialized the database')
    init_db()


if __name__ == '__main__':
    init()
