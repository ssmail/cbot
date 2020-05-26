# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong

import datetime

from sqlalchemy import UniqueConstraint

from mantis import db
from sqlalchemy.orm import class_mapper


class Slack(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workspace = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(64))
    token = db.Column(db.String(256))
    cookie = db.Column(db.String(256))

    __table_args__ = (
        UniqueConstraint('username', 'workspace', name='user_work_space'),
    )

    date_created = db.Column(
        db.DateTime,
        default=datetime.datetime.now
    )

    date_updated = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.utcnow
    )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def serialize_all(self):
        columns = [c.key for c in class_mapper(self.__class__).columns]
        return dict((c, getattr(self, c)) for c in columns)

    def __repr__(self):
        return '[username:{}, password:{}]'.format(self.username, self.token)
