# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong
import datetime

from sqlalchemy.orm import class_mapper

from mantis import db


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(64), index=True, nullable=False)
    assignee = db.Column(db.String(64), index=True, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    summary = db.Column(db.String(64), nullable=False)
    properties = db.Column(db.String(64), nullable=False)
    testrail = db.Column(db.String(256))
    link = db.Column(db.String(64), nullable=False)
    case_id = db.Column(db.String(32))
    testrail_project_id = db.Column(db.String(32))

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
