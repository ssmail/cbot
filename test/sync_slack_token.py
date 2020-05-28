# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong

"""
this file will sync slack user token to my aws service
requirements:
    Python version - 3.7.7
    3rd library:
        typed_json_dataclass
        selenium

    pip3 install typed_json_dataclass selenium --user

"""
import os
import sys
import re
import urllib3
import requests
from dataclasses import dataclass

from selenium import webdriver
from typed_json_dataclass import TypedJsonMixin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class SlackUser:
    workspace: str
    username: str
    password: str
    description: str
    pmi: str


@dataclass
class AuthenticatedSlackUser(TypedJsonMixin):
    id: int
    workspace: str
    username: str
    password: str
    token: str
    cookie: str
    date_created: str
    date_updated: str


def update(username, password, workspace, token, cookie):
    resp = requests.post(SERVER_ADDRESS + "/account/update", data={
        "username": username,
        "password": password,
        "workspace": workspace,
        "token": token,
        "cookie": cookie
    })

    if resp.status_code == 200:
        print(f"success ==========》update slack user token : user: {username}")


class SlackAuthService:
    _get_token_url = 'https://app.slack.com/auth?app=client'

    def __init__(self):
        self.driver = webdriver.Chrome(CHROME_PATH)
        self.driver.implicitly_wait(20)
        self.driver.set_page_load_timeout(60)
        self.s = requests.session()

    def auth(self, slackUser):
        self.driver.get(f'https://{slackUser.workspace}.slack.com/#/')
        self.driver.find_element_by_id("email").send_keys(slackUser.username)
        self.driver.find_element_by_id("password").send_keys(slackUser.password)
        self.driver.find_element_by_id("signin_btn").click()

        self.driver.get(f'view-source:{self._get_token_url}')
        cookie = self.driver.get_cookie('d')['value']
        page_source = self.driver.page_source

        token = self._get_token(page_source)

        print("token", token)
        print("cookie", cookie)

        update(
            username=slackUser.username,
            password=slackUser.password,
            workspace=slackUser.workspace,
            token=token,
            cookie=cookie
        )

    @staticmethod
    def _get_token(text) -> str:
        try:
            return re.findall('token":"(.+?)"', text)[0]
        except Exception:
            raise Exception("Get Slack Token Failed")

    def quit(self):
        self.driver.quit()


# SERVER_ADDRESS = 'http://localhost:8000'
SERVER_ADDRESS = 'https://devslackbot.zoomdev.us/api'

# CHROME_PATH = 'C:\\Users\\admin\\jenkins\\workspace\\slack_token_sync\\chromedriver.exe'
CHROME_PATH = sys.argv[2]
print(CHROME_PATH)

if __name__ == '__main__':
    task_list_api = SERVER_ADDRESS + '/account/list?auth=ZytSVlBWc2swb2VGYlNXNklGR1Z1QT09'
    all_task = []
    try:
        all_task = requests.get(task_list_api).json()['all']
    except Exception as e:
        print(f'get task failed : {task_list_api}')

    for i in all_task:
        print(f"task user: {i['username']}, workspace: {i['workspace']}")

    for i in all_task:
        login_service = SlackAuthService()
        user = AuthenticatedSlackUser.from_dict(i)
        print(f"{user.username} ---->")
        try:
            login_service.auth(user)
        except Exception as e:
            print(f"Failed xxxxxxxxxx :{user.username}")
            print(e)
        finally:
            login_service.quit()
