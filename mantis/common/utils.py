# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong
import functools
import re

import flask
from flask import request
from werkzeug.exceptions import BadRequest

from mantis.common.user import ZoomMessage


def require(*required_args):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            request_param = []
            if request.method == "POST":
                try:
                    request_param = request.json
                except BadRequest as e:
                    request_param = None
            elif request.method == "GET":
                request_param = request.args

            for arg in required_args:
                if not request_param or arg not in request_param:
                    return flask.jsonify(code=400, message='[{}] is necessary'.format(arg))

            return func(*args, **kw)

        return wrapper

    return decorator


def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results


def build_message(resp, workspace):
    dict_message = {
        'workspace': workspace,
        'userId': ensure_value(resp, 'authed_users'),
        "channel": get_value(resp, "channel"),
        "title": get_value(resp, "name"),
        "meetingId": get_value(resp, "display_id"),
        "messageType": get_value(resp, "type"),
        "subtype": get_value(resp, "subtype"),
        "text": get_value(resp, "text", 1),
        "password": get_password(get_value(resp, "text", 1)),
        'dateStart': get_value(resp, "ts"),
        'botId': get_value(resp, "bot_id"),
        'createBy': get_value(resp, "created_by"),
    }

    return ZoomMessage(**dict_message)


def get_password(text) -> str:
    return extract_info_from_text(r"assword\s*:\s(\w+)", text)


def extract_info_from_text(re_str, text):
    if text:
        try:
            return re.findall(re_str, text)[0]
        except IndexError:
            pass

    return ""


def get_value(j, key, index=0):
    try:
        return extract_values(j, key)[index]
    except:
        return ""


def ensure_value(j, key):
    try:
        return j[key][0]
    except:
        return ""


def auth(*args, **kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            if request.args.get("auth") == "ZytSVlBWc2swb2VGYlNXNklGR1Z1QT09":
                return func(*args, **kw)
            else:
                return flask.jsonify(code=400, message="auth error")

        return wrapper

    return decorator
