# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong
from dataclasses import dataclass


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
    date_start: str
    bot_id: str
    create_by: str


def build_message(resp):
    dict_message = {
        'user_id': resp['authed_users'][0],
        "channel": get_value(resp, "channel"),
        "title": get_value(resp, "text"),
        "meeting_id": get_value(resp, "display_id"),
        "message_type": get_value(resp, "type"),
        "subtype": get_value(resp, "subtype"),
        "password": get_value(resp, "text", 1),
        'date_start': get_value(resp, "ts"),
        'bot_id': get_value(resp, "bot_id"),
        'create_by': get_value(resp, "created_by"),
    }

    print(dict_message)
    zoom_message = ZoomVisibleMessage(**dict_message)
    return zoom_message


def get_value(j, key, index=0):
    try:
        l = extract_values(j, key)
        return l[index]
    except:
        return ""
