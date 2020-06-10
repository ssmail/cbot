# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong
import os
from enum import Enum


class TestrailProjectMapping(Enum):
    WEB = 2
    INTEGRATION = 31
    MARKETPLACE = 32


class TestRailAccount:
    server = "https://zoomus.testrail.io/"
    username = os.getenv("TESTRAIL_USERNAME")
    password = os.getenv("TESTRAIL_PASSWORD")


class JiraAccount:
    username = os.getenv("JIRA_USERNAME")
    token = os.getenv("JIRA_TOKEN")
