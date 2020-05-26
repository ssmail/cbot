# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
from flask import jsonify, request, Blueprint
from mantis.common.utils import require
from mantis.models.resp import RespCode, RespData
from mantis.models.user import User


"""
GET request param:
---->  username = request.args.get("username")
  
POST request param:
---->  username = request.json.get("username")
"""

test_api = Blueprint('test', __name__, url_prefix="/test")


@test_api.route("/test_url", methods=["POST", 'GET'])
@require("username")
def test_url():
    username = request.args.get("username")

    user = User.query.filter_by(username="admin").first()

    data = {
        "param": user.serialize_all
    }

    return RespData(RespCode.SUCCESS, data, message="test")


@test_api.route("/get_get_param", methods=["POST", 'GET'])
@require("username")
def get_get_param():
    username = request.args.get("username")

    user = User.query.filter_by(username="admin").first()

    data = {
        "param": user.serialize_all
    }

    return RespData(RespCode.SUCCESS, data, message="test")


@test_api.route("/get_post_param", methods=["POST", 'GET'])
@require("username")
def get_post_param():
    username = request.json.get("username")

    data = {
        "param": username
    }

    return RespData(RespCode.SUCCESS, data, message="test")


"""
a decorate check request param
support post and get request

http://localhost:5000/dev-api/test_require_param
"""


@test_api.route("/test_require_param", methods=["POST", 'GET'])
@require("username")
def test_require_param():
    username = request.args.get("username")

    data = {
        "param": username
    }

    return RespData(RespCode.SUCCESS, data, message="test")


"""
Serialize object:

serialize specific field
http://localhost:5000/dev-api/test_serialize

serialize model all field
http://localhost:5000/dev-api/test_serialize_all

"""


@test_api.route("/test_serialize")
def test_serialize():
    user = User.query.filter_by(username="admin").first()
    users = [user.serialize]
    r = {"users": users}
    return RespData(RespCode.SUCCESS, r)


@test_api.route("/test_serialize_all")
def test_serialize_all():
    user = User.query.filter_by(username="admin").first()
    r = {"user": user.serialize_all}
    return RespData(RespCode.SUCCESS, r)


"""
Cache function result:
http://localhost:5000/dev-api/test_mem_cache
http://localhost:5000/dev-api/test_cache
"""


"""
# celery task queue demo, send mail message async
http://localhost:5000/test/sendMessage?text=thisisatest
"""


