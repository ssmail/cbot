from dataclasses import dataclass

import requests
import urllib3
from flask import Blueprint, jsonify, request
from requests.auth import HTTPBasicAuth
from testrail_api import TestRailAPI

from mantis.models.Issue import Issue
from mantis.service.jiraapi import JiraService
from mantis.service.testrail import TestRailService

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

jira_api = Blueprint('jira', __name__, url_prefix='/qa/')
api = TestRailAPI("https://zoomus.testrail.io/", "carter.hong@zoom.us", "Zoom.156233")

url = "https://zoomvideo.atlassian.net/rest/api/3/search"

auth = HTTPBasicAuth("carter.hong@zoom.us", "5oRaeHI6F1zsswr4Aril1CCD")
s = requests.session()

headers = {
    "Accept": "application/json"
}

jira_service = JiraService()

testrail = TestRailService()


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
        return "WEB"
    elif project_name.startswith("integration"):
        return "INTEGRATION"
    elif project_name.startswith("marketplace"):
        return "MARKETPLACE"
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


@jira_api.route("/ep/issue")
def ep_issues():
    fix_version = request.args.get("fix_version", None)
    total = request.args.get("total", 100)

    if not fix_version:
        return jsonify({"error": "fix_version params should not be null"})

    issues = jira_service.query_issues(fix_version)

    issue_list = []
    for issue in issues:
        issue = Issue(
            key=issue['key'],
            assignee=tidy_name(get_path(issue, ['fields', 'assignee', "displayName"])),
            summary=get_path(issue, ["fields", 'summary']),
            properties=get_path(issue, ['fields', 'priority', 'name']),
            status=get_path(issue, ['fields', 'status', 'name']),
            testrail=get_path(issue, ['fields', 'customfield_12501']),
            link="https://zoomvideo.atlassian.net/browse/{}".format(issue['key'])
        )

        issue_list.append(issue.serialize_all)

    return jsonify(
        {
            "total": len(issue_list),
            "issues": issue_list,
            "code": 20000
        }
    )


@jira_api.route("/ep")
def ep():
    project = request.args.get("project", None)
    total = request.args.get("total", 100)

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


@jira_api.route("/ep/milestone", methods=['POST'])
def create():
    return jsonify(
        {
            "args": request.args,
            "json": request.json,
            "form": request.form
        }
    )
    #
    # if not ep_name:
    #     return jsonify({"error": "fix_version params should not be null"})
    #
    # projects = jira_service.query_project(ep_name)
    #
    # project_list = []
    #
    # for project in projects:
    #     project = EP(
    #         id=project['id'],
    #         description=get_path(project, ['description']),
    #         name=get_path(project, ["name"]),
    #         released=get_path(project, ['released']),
    #         releaseDate=get_path(project, ['releaseDate']),
    #         link='https://zoomvideo.atlassian.net/projects/ZOOM/versions/{}/tab/release-report-all-issues'.format(
    #             project['id'])
    #     )
    #     project_list.append(project)
    #
    # return jsonify(
    #     {
    #         "total": len(project_list),
    #         "fixVersions": project_list,
    #         "info": projects,
    #         "code": 20000
    #     }
    # )
