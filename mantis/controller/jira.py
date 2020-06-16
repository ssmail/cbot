import re
from dataclasses import dataclass

from flask import Blueprint, jsonify, request
from testrail_api import TestRailAPI

from mantis.config.testrail import TestrailProjectMapping, TestRailAccount
from mantis.models.Issue import Issue
from mantis.service.jiraapi import JiraService

jira_api = Blueprint('jira', __name__, url_prefix='/qa/')

api = TestRailAPI(TestRailAccount.server, TestRailAccount.username, TestRailAccount.password)

jira_service = JiraService()


def build_query(fix_version: str, max_results: int):
    query = {
        'jql': 'project = ZOOM AND fixVersion = "{}" ORDER BY priority DESC'.format(fix_version),
        "maxResults": max_results
    }
    return query


def tidy_name(text):
    if text:
        return text.replace(" ", ".").lower()
    else:
        return text


def get_path(data, path, default=None):
    try:
        for item in path:
            data = data[item]
        return data
    except (KeyError, TypeError, IndexError):
        return default


def convert_project(project_name: str):
    project_name = project_name.lower()

    if project_name.startswith("web"):
        return TestrailProjectMapping.WEB.value
    elif project_name.startswith("integration"):
        return TestrailProjectMapping.INTEGRATION.value
    elif project_name.startswith("marketplace"):
        return TestrailProjectMapping.MARKETPLACE.value
    else:
        return None


def get_case_by_section(project_id, section_id):
    s = api.cases.get_cases(project_id=project_id, section_id=section_id, limit=10)
    return [i['id'] for i in s]


@dataclass
class EP:
    id: int
    name: str
    releaseDate: str
    released: str
    description: str
    link: str


@jira_api.route('/', methods=['POST', 'GET'])
def index():
    return jsonify(
        {
            "args": request.args,
            "json": request.json,
            "form": request.form,
        }
    )


def fetch_case_id(link):
    if link:
        if 'suites/view' in link.lower():
            return "suite_group:" + re.findall('group_id=(\d+)', link)[0]
        if 'cases/view' in link.lower():
            return re.findall('cases\/view\/(\d+)', link)[0]
        elif 'group_id' in link.lower():
            return "group:" + re.findall('group_id=(\d+)', link)[0]
        elif 'tests/view' in link.lower():
            return "tests:" + re.findall('tests\/view\/(\d+)', link)[0]
    else:
        return ""


@jira_api.route("/ep/reviewCase", methods=['POST'])
def review():
    fix_version = request.form.get("fix_version", None)
    jira_key = request.form.get("case", None)

    print(fix_version)
    print(jira_key)

    all = Issue.query.all()

    case: Issue = Issue.query.filter_by(
        fix_version=fix_version,
        key=jira_key
    ).first()

    for i in all:
        print(i.serialize_all)

    print(case)

    if case:
        case.review = "review"
        case.save()
        return jsonify({"issue": case.serialize_all})
    else:
        return jsonify({"error": "issue not found"})


@jira_api.route("/ep/issue/query")
def query_ep_issues():
    fix_version = request.args.get("fix_version", None)
    assignee = request.args.get("assignee", None)

    print(fix_version)
    print(assignee)

    if not fix_version:
        return jsonify({"error": "fix_version params should not be null"})

    if assignee:
        all_issue = Issue.query.filter_by(
            assignee=assignee,
            fix_version=fix_version
        ).all()
    else:
        all_issue = Issue.query.filter_by(
            fix_version=fix_version
        ).all()

    temp = Issue.query.filter_by(
        fix_version=fix_version
    ).all()
    assignees = []
    for i in temp:
        if i.assignee not in assignees:
            assignees.append(i.assignee)

    return jsonify(
        {
            "total": len(all_issue),
            "issues": [i.serialize_all for i in all_issue],
            "assignees": assignees
        }
    )


@jira_api.route("/ep/issue/sync")
def sync_ep_issues():
    fix_version = request.args.get("fix_version", None)

    if not fix_version:
        return jsonify({"error": "fix_version params should not be null"})

    issues = jira_service.query_issues(fix_version)

    for issue in issues:
        assignee = tidy_name(get_path(issue, ['fields', 'assignee', "displayName"]))
        testrail = get_path(issue, ['fields', 'customfield_12501'])

        testrail_project_id = security_re(r'view\/(\d+)?\&', testrail)

        issue = Issue(
            key=issue['key'],
            assignee=assignee,
            fix_version=fix_version,
            summary=get_path(issue, ["fields", 'summary']),
            properties=get_path(issue, ['fields', 'priority', 'name']),
            status=get_path(issue, ['fields', 'status', 'name']),
            testrail=testrail,
            link="https://zoomvideo.atlassian.net/browse/{}".format(issue['key']),
            case_id=fetch_case_id(get_path(issue, ['fields', 'customfield_12501'])),
            testrail_project_id=testrail_project_id
        )

        data_in_db = Issue.query.filter_by(
            key=issue.key,
            fix_version=issue.fix_version
        ).first()

        print(data_in_db)

        if not data_in_db:
            issue.save()
        else:
            print("================")

    all_issue = Issue.query.all()

    return jsonify(
        {
            "total": len(all_issue),
            "issues": [i.serialize_all for i in all_issue],
            "code": 20000
        }
    )


@jira_api.route("/ep/caseReviewProgress", methods=['GET'])
def caseReviewProgress():
    fix_version = request.args.get("fixVersion")

    review_case = Issue.query.filter_by(
        review="review",
        fix_version=fix_version
    ).count()

    not_review = Issue.query.filter_by(
        review="not_review",
        fix_version=fix_version
    ).count()

    try:
        percentage = round(review_case * 100 / (review_case + not_review), 2)
    except:
        percentage = 0

    return jsonify(
        {
            "review": review_case,
            "notReview": not_review,
            "total": review_case + not_review,
            "percentage": percentage
        }
    )


@jira_api.route("/ep")
def ep():
    project = request.args.get("project", None)

    if not project:
        return jsonify({"error": "project params should not be null"})

    projects = jira_service.query_project(project)

    project_list = []

    for project in projects:
        project = EP(
            id=project['id'],
            description=get_path(project, ['description']),
            name=get_path(project, ["name"]),
            released=get_path(project, ['released']),
            releaseDate=get_path(project, ['releaseDate']),
            link='https://zoomvideo.atlassian.net/projects/ZOOM/versions/{}/tab/release-report-all-issues'.format(
                project['id'])
        )
        project_list.append(project)

    return jsonify(
        {
            "total": len(project_list),
            "fixVersions": project_list,
            "info": projects,
            "code": 20000
        }
    )


def get_case_id(project_id, case_info):
    if not case_info:
        return []
    if case_info.startswith("suite_group"):
        section_id = int(case_info.replace("suite_group:", ""))
        real_project_id = api.suites.get_suite(project_id)['project_id']
        return [case['id'] for case in api.cases.get_cases(real_project_id, suite_id=project_id, section_id=section_id)]
    if case_info.startswith("group:"):
        section_id = int(case_info.replace("group:", ""))
        print(section_id, project_id)
        return [case['id'] for case in api.cases.get_cases(project_id, section_id=section_id)]
    elif case_info.startswith("test:"):
        return [case['id'] for case in api.results.get_results(int(case_info.replace("test:", "")))]
    else:
        return [case_info]


def security_re(r, text):
    try:
        return re.findall(r, text)[0]
    except:
        return ""


@jira_api.route("/ep/milestone", methods=['POST', 'GET', 'OPTIONS'])
def create():
    fix_version = request.form.get("fix_version", None)

    if not fix_version:
        return jsonify({"error": "fix_version params should not be null"})

    issues = jira_service.query_issues(fix_version)

    issue_list = {}
    for issue in issues:
        assignee = tidy_name(get_path(issue, ['fields', 'assignee', "displayName"]))
        testrail = get_path(issue, ['fields', 'customfield_12501'])

        if not testrail:
            continue

        testrail_project_id = security_re(r'view\/([\d]{1,3})?\&', testrail)

        if not testrail_project_id:
            testrail_project_id = convert_project(fix_version)

        print("====> ", testrail, testrail_project_id)

        issue = Issue(
            key=issue['key'],
            assignee=assignee,
            summary=get_path(issue, ["fields", 'summary']),
            properties=get_path(issue, ['fields', 'priority', 'name']),
            status=get_path(issue, ['fields', 'status', 'name']),
            testrail=testrail,
            link="https://zoomvideo.atlassian.net/browse/{}".format(issue['key']),
            case_id=fetch_case_id(get_path(issue, ['fields', 'customfield_12501'])),
            testrail_project_id=testrail_project_id
        )

        if assignee in issue_list:
            issue_list[assignee].append(issue.serialize_all)
        else:
            issue_list[assignee] = []
            issue_list[assignee].append(issue.serialize_all)

    for assignee, issue in issue_list.items():
        id_list = []
        for case in issue:
            print(case['testrail'], case['case_id'], case['testrail_project_id'])
            case_tmp_list = get_case_id(case['testrail_project_id'], case['case_id'])
            id_list = id_list + case_tmp_list

        print(assignee, id_list)

        # my_test_run = api.runs.add_run(
        #     project_id=2,
        #     name=assignee + "_test_auto_add_by_api",
        #     milestone_id=1742,
        #     include_all=False,
        #     case_ids=id_list
        # )

    return jsonify({"a": "b"})
