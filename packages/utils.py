# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong
import json
import re
from dataclasses import dataclass

from sqlalchemy.orm import class_mapper


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


@dataclass
class ZoomVisibleMessage:
    user_id: str
    channel: str
    title: str
    meeting_id: str
    message_type: str
    subtype: str
    password: str
    password_text: str
    date_start: str
    bot_id: str
    create_by: str


def build_message(resp):
    dict_message = {
        'user_id': resp['authed_users'][0],
        "channel": get_value(resp, "channel"),
        "title": get_value(resp, "name"),
        "meeting_id": get_value(resp, "display_id"),
        "message_type": get_value(resp, "type"),
        "subtype": get_value(resp, "subtype"),
        "password_text": get_value(resp, "text", 1),
        "password": get_password(get_value(resp, "text", 1)),
        'date_start': get_value(resp, "ts"),
        'bot_id': get_value(resp, "bot_id"),
        'create_by': get_value(resp, "created_by"),
    }

    return ZoomVisibleMessage(**dict_message)


def get_password(text) -> str:
    return extract_info_from_text(r"password:\s(\w+)", text)


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
