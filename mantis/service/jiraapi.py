# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong


import requests
from requests.auth import HTTPBasicAuth

from mantis.config.testrail import JiraAccount


class JiraService:
    auth = HTTPBasicAuth(JiraAccount.username, JiraAccount.token)

    headers = {
        "Accept": "application/json"
    }

    def query_issues(self, fix_version):
        url = "https://zoomvideo.atlassian.net/rest/api/3/search"

        jql = f'project = "ZOOM" AND fixVersion = "{fix_version}"'

        query = {'jql': jql, "maxResults": "200"}

        response = requests.request(
            "GET",
            url,
            headers=self.headers,
            params=query,
            auth=self.auth
        )

        issues = response.json()
        print("---> ", issues['total'])
        return issues['issues']

    def query_project(self, text):
        url = 'https://zoomvideo.atlassian.net/rest/api/2/project/ZOOM/version'

        params = (
            ('expand', 'issuesstatus'),
            ('maxResults', '100'),
            ('orderBy', '-sequence'),
            ('query', text),
            ('startAt', '0'),
            # ('status', 'unreleased'),
        )

        response = requests.request(
            "GET",
            url,
            headers=self.headers,
            params=params,
            auth=self.auth
        )

        issues = response.json()['values']

        return issues


if __name__ == '__main__':
    jira = JiraService()
    jira.query_issues("Web-EP-20200607 For US04")
    jira.query_project('0607')
