# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong
import re
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
    workspace: str
    userId: str
    channel: str
    title: str
    meetingId: str
    message_type: str
    subtype: str
    password: str
    text: str
    dateStart: str
    botId: str
    createBy: str


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

    return ZoomVisibleMessage(**dict_message)


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
