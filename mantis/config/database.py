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
PASSWORD = '.Carter0410'
HOST = '10.100.83.189'
PORT = 3306
DATABASE = 'skyline_dev'

# SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
#     DIALECT,
#     DRIVER,
#     USERNAME,
#     PASSWORD,
#     HOST,
#     PORT,
#     DATABASE
# )

file_path = os.path.abspath(os.getcwd()) + "/db/database.db"

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
# SQLALCHEMY_TRACK_MODIFICATIONS = False
