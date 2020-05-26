# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
import os
from dataclasses import dataclass

success = "success"
message = "message"
result = "result"
data = "data"


@dataclass
class MailConfig:
    to_mail = "806005290@qq.com"
    send_mail_from = 'antsync@163.com'
    send_mail_smtp = 'smtp.163.com'
    send_mail_password = "hc299792458"


class ParamErrorStr:

    @staticmethod
    def param_missing(param_key):
        param_missing_message = "request param [{}] is missing"
        return {
            success: False,
            message: param_missing_message.format(param_key)
        }
