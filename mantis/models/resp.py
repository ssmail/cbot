# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
import dataclasses
import json
from pprint import pprint
from typing import Dict
from enum import Enum

from flask import jsonify, make_response
from sqlalchemy.orm import class_mapper


class RespCode(Enum):
    SUCCESS = 200
    FAILED = 201


def json_object(cls):
    def wrapper(*args, **kwargs):
        retval = cls(*args, **kwargs)

        if "message" in retval.__dict__.keys():
            return {"code": retval.code.value, "data": retval.data, "message": retval.message}
        else:
            return {"code": retval.code.value, "data": retval.data}

    return wrapper


@json_object
class RespData:
    def __init__(self, code: RespCode, data, **kwargs):
        self.code = code
        self.data = data

        if kwargs:
            self.message = kwargs.get("message", None)

    def __repr__(self):
        return "code:", self.code, "self.message: ", self.message
