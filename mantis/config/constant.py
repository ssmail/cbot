# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong


class Auth:
    TOKEN_EXPIRE_DATE = 30

    TOKEN_NAME = "b_token"
    USERNAME = "username"
    LOGOUT = {"success": True, "message": "logout success"}
    AUTH_FAILED = {"AUTH FAILED": "Login Check Failed"}
    LOGIN_PARAM_ERROR = {"AUTH FAILED": "Login Params error"}
    LOGIN_FAILED = {"code": 403, "message": "Login Failed"}
    AUTH_SUCCESS = {"code": 200, "data": {"token": "admin-token"}}


class AuthStatus:
    Forbidden = 401


class AuthWhiteList:
    URL_PATH = [
        "/user/login",
        "/user/logout",
        "/user/add",
        "/test_serialize",
        "/test_mem_cache",
        "/user/query"
    ]


class LogConfig:
    LogCfg = """
version: 1
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout
  file:
    class: logging.FileHandler
    level: INFO
    formatter: simple
    filename: app.log
loggers:
  console:
    level: DEBUG
    handlers: [console]
    propagate: no
  file:
    level: DEBUG
    handlers: [file]
    propagate: no
root:
  level: DEBUG
  handlers: [console,file]
    """
