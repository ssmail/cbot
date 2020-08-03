# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong

import logging.config
from datetime import date

import yaml
from flasgger import Swagger
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


app = Flask("mantis")
swagger = Swagger(app)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# redis server
redis_server = "localhost"
# redis_server = "172.19.14.16"

# task task queue redis
app.config['CELERY_BROKER_URL'] = 'redis://{}:6379/0'.format(redis_server)

# task task result redis
app.config['CELERY_RESULT_BACKEND'] = 'redis://{}:6379/0'.format(redis_server)

# auto format datetime
app.json_encoder = CustomJSONEncoder

# auto format Dict to jsonify
# app.response_class = JSONResponse

# init task

# init db
db = SQLAlchemy(app)

logging.config.dictConfig(yaml.load(LogConfig.LogCfg, Loader=yaml.FullLoader))
logging.getLogger("testrail_api").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING)
# base server api
from mantis import interceptor

# other api
# from mantis.controller.api import test_api
from mantis.controller.user import user_api
from mantis.controller.account import account_api
from mantis.controller.slack import slack_api
from mantis.controller.jira import jira_api
from mantis.controller.cluster import cluster_api
from mantis.controller.epic import epic_api

# app.register_blueprint(test_api)
app.register_blueprint(user_api)
app.register_blueprint(account_api)
app.register_blueprint(slack_api)
app.register_blueprint(jira_api)
app.register_blueprint(cluster_api)
app.register_blueprint(epic_api)

app.debug = True
app.config['CORS_HEADERS'] = 'Content-Type'

Base = declarative_base()
db.create_all()
