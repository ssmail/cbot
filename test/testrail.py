# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong

from testrail_api import TestRailAPI

# my_test_run = api.runs.add_run(
#     project_id=2,
#     name="My test run",
#     milestone_id=1742,
#     include_all=False,
#     case_ids=['56782955', '56782956', '56782957']
# )
#
# for i in my_test_run.items():
#     print(i)
from mantis.config.testrail import TestRailAccount

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
# for i in suites.items():
#     print(i)

if __name__ == '__main__':
    api = TestRailAPI("https://zoomus.testrail.io/", TestRailAccount.username, TestRailAccount.password)

    # cases = api.cases.get_cases(2, section_id=99041016)
    # cases = api.cases.get_cases(2, section_id=56778576)

    # case = api.cases.get_case(56778576)
    # print(case)
    # result = api.results.get_results(99041016)
    # print(result)

    # for i in cases:
    #     print(i['id'])

    # case = api.cases.get_cases(2, section_id=7678186)
    # print(case)

    # https://zoomus.testrail.io/index.php?/tests/view/99041016

    # https://zoomus.testrail.io/index.php?/cases/view/56778576

    # https://zoomus.testrail.io/index.php?/suites/view/11&group_by=cases:section_id&group_id=7678369&group_order=asc

    # a = api.cases.get_cases(9, suite_id=11, section_id=7678369)
    # for i in a:
    #     print(a)
    print(api.suites.get_suite(11)['project_id'])
