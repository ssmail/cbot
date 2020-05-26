# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
import requests

from utils.common import ignore_exception, function_time_usage
from utils.const import MailConfig
from utils.notify import MailService
from utils.log import SimpleLog


def add_user():
    data = {
        "username": "",
        "password": "",
        "workspace": "",
        "token": "",
        "cookie": ""
    }
    resp = requests.post("https://devslackbot.zoomdev.us/api/account/add", data=data).json()
    print(resp)


add_user()
