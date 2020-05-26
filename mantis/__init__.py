# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong

import logging, logging.config, yaml
from datetime import date

import yaml

from flask import Flask, Response
from flask.json import JSONEncoder, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

from mantis.config.constant import LogConfig
from mantis.config.database import SQLALCHEMY_DATABASE_URI
from mantis.models.resp import RespData


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class JSONResponse(Response):
    default_mimetype = 'application/json'

    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)
            return super(JSONResponse, cls).force_type(response, environ)


mantis_server = Flask("mantis")

mantis_server.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
mantis_server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mantis_server.config['SQLALCHEMY_ECHO'] = False

# redis server
redis_server = "localhost"
# redis_server = "172.19.14.16"

# task task queue redis
mantis_server.config['CELERY_BROKER_URL'] = 'redis://{}:6379/0'.format(redis_server)

# task task result redis
mantis_server.config['CELERY_RESULT_BACKEND'] = 'redis://{}:6379/0'.format(redis_server)

# auto format datetime
mantis_server.json_encoder = CustomJSONEncoder

# auto format Dict to jsonify
mantis_server.response_class = JSONResponse

# init task

# init db
db = SQLAlchemy(mantis_server)

logging.config.dictConfig(yaml.load(LogConfig.LogCfg, Loader=yaml.FullLoader))

# base server api
from mantis import interceptor

# other api
from mantis.controller.api import test_api
from mantis.controller.user import user_api
from mantis.controller.account import account_api
from mantis.controller.slack import slack_api

mantis_server.register_blueprint(test_api)
mantis_server.register_blueprint(user_api)
mantis_server.register_blueprint(account_api)
mantis_server.register_blueprint(slack_api)
mantis_server.debug = True
