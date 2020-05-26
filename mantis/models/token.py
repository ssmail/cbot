# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
import datetime
from mantis import db
from sqlalchemy.orm import class_mapper


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(64), index=True, unique=True)
    token = db.Column(db.String(64), unique=True)
    expire_datetime = db.Column(db.DateTime)

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

    def __repr__(self):
        return '[username:{}, token:{}]'.format(self.username, self.token)
