# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
import json
import time
from dataclasses import dataclass
from pprint import pprint

from flask import request, jsonify
from sqlalchemy.orm import class_mapper

from utils.const import ParamErrorStr
from utils.log import SimpleLog

log = SimpleLog()


def ignore_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.error(
                "ignore exception ---> [{}] has occur an exception:"
                " [{}], and this exception has ignored".format(
                    func.__name__, e.__class__.__name__
                )
            )

    return wrapper


def function_time_usage(func):
    def wrapper(*args, **kwargs):
        beg_ts = time.time()
        log.info("start exec func[{}]".format(func.__name__))
        ret_val = func(*args, **kwargs)
        end_ts = time.time()
        log.info("[{}] exec finished, cost time: {}".format(func.__name__, end_ts - beg_ts))
        return ret_val

    return wrapper


def parse(o):
    columns = [c.key for c in class_mapper(o.__class__).columns]
    return dict((c, getattr(o, c)) for c in columns)


@dataclass
class Pager:
    size: int = 10
    page: int = 0

    @property
    def offset(self):
        return self.page * self.size


def pager():
    page = request.args.get("page")
    size = request.args.get("size")

    if not size: size = 10
    if not page: page = 1

    return page, size
