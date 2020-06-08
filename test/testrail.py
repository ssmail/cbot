# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong

from testrail_api import TestRailAPI

api = TestRailAPI("https://zoomus.testrail.io/", "carter.hong@zoom.us", "Zoom.156233")

# def add_milestore():
#     new_milestone = api.milestones.add_milestone(
#         project_id=2,
#         name="AutoCreateByCarterApiadds",
#         start_on=int(datetime.now().timestamp()),
#         parent_id=1741
#     )
#

# add_milestore()

# m = api.milestones.get_milestone(1743)

# my_test_run = api.runs.add_run(
#     project_id=2,
#     suite_id=2,
#     name="My test run",
#     include_all=True,
#     milestone_id=m["id"]
# )

# user = api.users.get_user_by_email("Lemon.Wu@zoom.us")
#
# print(user)


# sections = api.sections.get_sections(31)
#
# for i in sections:
#     if i['name'] == 'IntegrationService-EP-20200607':
#         print(i)
#         break

cases = api.cases.get_cases(2, section_id=7682782)

for i in cases:
    print(i['id'])

# for i in suites.items():
#     print(i)


my_test_run = api.runs.add_run(
    project_id=2,
    name="My test run",
    milestone_id=1742,
    include_all=False,
    case_ids=['56782955', '56782956', '56782957']
)

for i in my_test_run.items():
    print(i)
