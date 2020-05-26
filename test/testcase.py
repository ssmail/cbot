# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
import requests

from utils.common import ignore_exception, function_time_usage
from utils.const import MailConfig
from utils.notify import MailService
from utils.log import SimpleLog


def mail_test():
    with MailService("hongchris@qq.com") as ms:
        ms.send("TEST", image_list=['a.jpg'])


def add_user():
    for i in range(1, 2):
        resp = requests.get(
            'http://localhost:5000/dev-api/user/add?username=admin12{}&email=123@qq.com'.format(i)
        )
        print(resp.status_code)

