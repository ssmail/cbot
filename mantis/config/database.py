# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
import os

DEBUG = True
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'remote'
PASSWORD = 'WDremote.123456'
HOST = '10.37.34.3'
PORT = 3306
DATABASE = 'flask'
#
# SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
#     DIALECT,
#     DRIVER,
#     USERNAME,
#     PASSWORD,
#     HOST,
#     PORT,
#     DATABASE
# )

file_path = os.path.abspath(os.getcwd()) + "/database.db"

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
SQLALCHEMY_TRACK_MODIFICATIONS = False
