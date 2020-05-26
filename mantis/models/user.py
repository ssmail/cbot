# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong

import datetime

from sqlalchemy import inspect

from mantis import db
from sqlalchemy.orm import class_mapper


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=False)
    password = db.Column(db.String(128), nullable=False, default="123456")

    date_created = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        nullable=False
    )

    date_updated = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }

    @property
    def serialize_all(self):
        columns = [c.key for c in class_mapper(self.__class__).columns]
        return dict((c, getattr(self, c)) for c in columns)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def valid(self):

        if len(self.username) < 4:
            return False

        if '@' not in self.email:
            return False

        return True
