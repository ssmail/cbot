# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong
from dataclasses import dataclass
from datetime import datetime
from typing import List

from testrail_api import TestRailAPI
from typed_json_dataclass import TypedJsonMixin

from mantis.config.testrail import TestRailAccount


@dataclass
class Project(TypedJsonMixin):
    id: int
    name: str
    url: str
    announcement: str
    show_announcement: bool
    is_completed: bool
    completed_on: str
    suite_mode: int


@dataclass
class Milestone(TypedJsonMixin):
    id: int
    name: str
    description: str
    started_on: str
    start_on: int
    is_started: bool
    due_on: str
    is_completed: bool
    completed_on: str
    project_id: int
    parent_id: int
    url: str
    milestones: List[str]


class TestRailService:

    @staticmethod
    def add_milestone(project_id, milestone_name):
        new_milestone = api.milestones.add_milestone(
            project_id=project_id,
            name=milestone_name,
            start_on=int(datetime.now().timestamp()),
        )
        print(new_milestone)

    @staticmethod
    def add_sub_milestone(project_id, milestone_name, parent_id):
        new_milestone = api.milestones.add_milestone(
            project_id=2,
            name=milestone_name,
            start_on=int(datetime.now().timestamp()),
            parent_id=1741
        )
        return Milestone.from_dict(new_milestone)

    @staticmethod
    def add_test_run():
        pass


if __name__ == '__main__':
    api = TestRailAPI(TestRailAccount.server, TestRailAccount.username, TestRailAccount.password)

    # s = TestRailService()
    # s.add_sub_milestone(2, "add_by_s_2", 123)
