# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong
import json

import requests
from requests.auth import HTTPBasicAuth


class JiraService:
    auth = HTTPBasicAuth("carter.hong@zoom.us", "5oRaeHI6F1zsswr4Aril1CCD")

    headers = {
        "Accept": "application/json"
    }

    def query_issues(self, fix_version):
        url = "https://zoomvideo.atlassian.net/rest/api/3/search"

        jql = f'project = ZOOM AND fixVersion = "{fix_version}" ORDER BY priority DESC'

        query = {
            'jql': jql
        }

        response = requests.request(
            "GET",
            url,
            headers=self.headers,
            params=query,
            auth=self.auth
        )

        issues = response.json()

        for issue in issues['issues']:
            print(issue)

    def query_project(self, text):
        url = 'https://zoomvideo.atlassian.net/rest/api/2/project/ZOOM/version'

        params = (
            ('expand', 'issuesstatus'),
            ('maxResults', '25'),
            ('orderBy', '-sequence'),
            ('query', text),
            ('startAt', '0'),
            ('status', 'unreleased'),
        )

        response = requests.request(
            "GET",
            url,
            headers=self.headers,
            params=params,
            auth=self.auth
        )

        issues = response.json()['values']

        for issue in issues:
            print(issue)


# jira = JiraService()
# jira.query_issues("Web-EP-20200607 For US04")
# jira.query_project('0607')

resp = requests.post('http://localhost:8000/qa/ep/milestone', json={"a": "b"}).text
print(resp)
