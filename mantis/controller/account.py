# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
from flask import jsonify, request, Blueprint

from mantis.common.utils import require
from mantis.models.slack import Slack

account_api = Blueprint('account', __name__, url_prefix='/account')


@account_api.route('/', methods=['POST', 'GET'])
def index():
    return jsonify(
        {
            "args": request.args,
            "json": request.json,
            "form": request.form,
        }
    )


@account_api.route('/list', methods=['POST', 'GET'])
def list_all():
    all_account = Slack.query.all()
    return jsonify({"all": [slack.serialize_all for slack in all_account]})


@account_api.route('/query', methods=['POST', 'GET'])
@require("username", "workspace")
def query_by():
    username = request.args.get("username")
    workspace = request.args.get("workspace")

    user = Slack.query.filter_by(
        username=username,
        workspace=workspace
    ).first()

    if not user:
        return jsonify({"data": "not found"})
    else:
        return jsonify({"slack": user.serialize_all})


@account_api.route('/update', methods=['POST', 'GET'])
@require("username", "workspace")
def update():
    username = request.json.get("username")
    workspace = request.json.get("workspace")
    password = request.json.get("password")

    cookie = request.json.get("cookie")
    token = request.json.get("token")

    user = Slack.query.filter_by(
        username=username,
        workspace=workspace
    ).first()

    if not user:
        new_user = Slack()
        new_user.username = username
        new_user.password = password
        new_user.workspace = workspace
        new_user.cookie = cookie
        new_user.token = token

        new_user.save()
        return jsonify({"create success": new_user.serialize_all})
    else:
        user.password = password
        user.cookie = cookie
        user.token = token

        user.save()

        return jsonify({"update success": user.serialize_all})


@account_api.route("/add", methods=['POST', 'GET'])
def add():
    username = request.json.get("username")
    password = request.json.get("password")
    workspace = request.json.get("workspace")
    token = request.json.get("token")
    cookie = request.json.get("cookie")

    slack = Slack(
        username=username,
        password=password,
        workspace=workspace,
        token=token,
        cookie=cookie,
    )

    slack.save()

    return jsonify({"slack": slack.serialize_all})
