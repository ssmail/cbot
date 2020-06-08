# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong

import datetime

from sqlalchemy.orm import class_mapper

from mantis import db


class EP(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ep_name = db.Column(db.String(64), index=True, nullable=False)
    team = db.Column(db.String(64), index=True, nullable=False)
    site = db.Column(db.String(64), nullable=False)

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
        return '[ep_name:{}]'.format(self.ep_name)
