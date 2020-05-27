# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong

import datetime
import json
import uuid
from pprint import pprint
from flask import make_response, request

from mantis import app
from mantis.config.constant import Auth, AuthStatus, AuthWhiteList
from mantis.models.resp import RespCode, RespData
from mantis.models.token import Token
from mantis.models.user import User
from utils.common import ignore_exception

# http://locahost:/test/  equals http://localhost/test
# url has no / sensitive
app.url_map.strict_slashes = False


def auth_intercept():
    if request.path in AuthWhiteList.URL_PATH:
        return True

    if '/sockjs-node/' in request.path:
        return True

    # b_token = request.cookies.get('b_token', None)
    # b_username = request.cookies.get('username', None)
    #
    # token = Token.query.filter_by(username=b_username).first()
    #
    # now = datetime.datetime.today()

    # login will check following item
    # 1. token exist
    # 2. token correct
    # 3. token not expired
    # return True or token and token.token == b_token and token.expire_datetime > now

    return request.headers.get("Query-Key") == "ZytSVlBWc2swb2VGYlNXNklGR1Z1QT09"


@app.route("/user/logout", methods=['POST', 'GET'])
def logout():
    b_token = request.cookies.get(Auth.TOKEN_NAME, None)
    b_username = request.cookies.get(Auth.USERNAME, None)

    # query token
    logout_user_token = Token.query.filter_by(username=b_username).first()

    # delete user token
    if logout_user_token:
        logout_user_token.delete()

    # logout response
    response = make_response(Auth.LOGOUT)

    # delete cookie
    response.delete_cookie(Auth.USERNAME)
    response.delete_cookie(Auth.TOKEN_NAME)

    return RespData(RespCode.SUCCESS, Auth.LOGOUT)


@app.route("/user/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        post_data = json.loads(request.get_data().decode("utf-8"))
        username = post_data.get("username", None)
        password = post_data.get("password", None)
    else:
        username = request.args.get("username", None)
        password = request.args.get("password", None)

    if not (username and password):
        return make_response(Auth.LOGIN_PARAM_ERROR), AuthStatus.Forbidden

    user = User.query.filter_by(
        username=username
    ).first()

    if user and user.password == password:
        token_value = uuid.uuid4().hex

        # make login response
        response = make_response(Auth.AUTH_SUCCESS)
        out_date = datetime.datetime.today() + datetime.timedelta(days=Auth.TOKEN_EXPIRE_DATE)

        response.set_cookie(Auth.TOKEN_NAME, token_value, expires=out_date)
        response.set_cookie(Auth.USERNAME, username, expires=out_date)

        token = Token.query.filter_by(username=username).first()

        if token:
            token.token = token_value
            token.expire_datetime = out_date
            token.save()
        else:
            # save token in db/dev/user/login
            new_token = Token(username=username, token=token_value, expire_datetime=out_date)
            new_token.save()

        return response, 200
    else:
        return make_response(Auth.LOGIN_FAILED), 200


@app.before_request
def login_filter():
    # all request will execute this flow

    # debug request basic info
    show_request_param()

    # login check
    if not auth_intercept():
        return make_response(Auth.AUTH_FAILED), AuthStatus.Forbidden


@ignore_exception
def show_request_param():
    if app.debug:
        if "sockjs-node" not in request.url:
            print(request.method, "jellyfish_service Url：" + str(request.path))
            if request.args: print("Param：" + json.dumps(request.args))
            if request.form: print("Param：" + str(request.form))


@ignore_exception
def show_response(environ):
    if app.debug:
        print("Response:\b")
        pprint(json.loads(environ.response[0].strip()))
        print("\n")


@app.after_request
def foot_log(environ):
    show_response(environ)
    return environ


@app.errorhandler(404)
def page_not_found(e):
    return make_response({"mantis_server request error": str(e)}), 404
