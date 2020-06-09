# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
from random import randint

from flask import jsonify, request, Blueprint
from flask_sqlalchemy import Pagination

from mantis import RespData
from mantis.models.resp import RespCode
from mantis.models.user import User
from utils.common import pager

user_api = Blueprint('user', __name__, url_prefix='/user')


@user_api.route('/')
def index():
    current_user = request.cookies.get("username", None)
    User.query.list_all()
    return jsonify({"result": User.query.list_all()})


@user_api.route('/query')
def query():
    page, size = pager()

    posts: Pagination = User.query.filter(
        User.username.isnot(None),
    ).order_by(
        User.id
    ).paginate(int(page), int(size), error_out=False)

    users = [user.serialize_all for user in posts.items]
    data = {"result": users, "totalCount": posts.total}

    return RespData(RespCode.SUCCESS, data)


@user_api.route('/user/queryBy')
def query_by():
    user = User.query.filter_by(
        username="username_{}".format(randint(1, 100000))
    ).first()

    if not user:
        return RespCode(RespCode.SUCCESS, {"data": "test"})

    data = {"result": user.serialize}

    return RespData(RespCode.SUCCESS, data)


@user_api.route("/add", methods=['POST', 'GET'])
def add():
    username = request.json.get("username")
    password = request.json.get("password")

    print(request.form)

    user = User(
        username=username,
        password=password
    )

    print(user)

    user.save()
    data = {"user": user.serialize_all}
    return RespData(RespCode.SUCCESS, {"data": data}, message="create user successfully")
