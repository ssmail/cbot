# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong
import logging
import os
import time
import urllib
import urllib.parse
from dataclasses import dataclass
from enum import Enum
from random import randint

import requests
import urllib3
from typed_json_dataclass import TypedJsonMixin

from mantis.config.config import ZoomRequestPayloadText

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)


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


@dataclass
class ZoomMessage(TypedJsonMixin):
    workspace: str
    user_id: str
    channel: str
    title: str
    meeting_id: str
    message_type: str
    subtype: str
    password: str
    text: str
    date_start: str
    bot_id: str
    create_by: str


class ZoomCommand(Enum):
    Zoom = 0, '/zoom'
    ZoomMeetingTopic = 1, '/zoom meeting ${topic}'
    ZoomJoinMe = 2, '/zoom join me'
    ZoomJoinMeetingId = 3, '/zoom join ${meetingId}'


def call_button(token, cookie, user, app):
    curl_template = '''curl -H 'Host: accountlevel.slack.com' -H 'Cookie: d=__COOKIE__;' -H 'pragma: no-cache' -H 'cache-control: no-cache' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36' -H 'dnt: 1' -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundaryy5A5abZY5Lw9fuaA' -H 'accept: */*' -H 'origin: https://app.slack.com' -H 'sec-fetch-site: same-site' -H 'sec-fetch-mode: cors' -H 'sec-fetch-dest: empty' -H 'accept-language: en,zh;q=0.9,zh-CN;q=0.8,ja;q=0.7,la;q=0.6,zh-TW;q=0.5' -H 'query-key: ZytSVlBWc2swb2VGYlNXNklGR1Z1QT09' -H 'web-guard: TAScript' --data-binary '------WebKitFormBoundaryy5A5abZY5Lw9fuaA
Content-Disposition: form-data; name="channel"

__USER__
------WebKitFormBoundaryy5A5abZY5Lw9fuaA
Content-Disposition: form-data; name="app"

__APP__
------WebKitFormBoundaryy5A5abZY5Lw9fuaA
Content-Disposition: form-data; name="type"

video
------WebKitFormBoundaryy5A5abZY5Lw9fuaA
Content-Disposition: form-data; name="token"

__TOKEN__
------WebKitFormBoundaryy5A5abZY5Lw9fuaA
Content-Disposition: form-data; name="_x_reason"

call-button-clicked
------WebKitFormBoundaryy5A5abZY5Lw9fuaA
Content-Disposition: form-data; name="_x_mode"

online
------WebKitFormBoundaryy5A5abZY5Lw9fuaA
Content-Disposition: form-data; name="_x_sonic"

true
------WebKitFormBoundaryy5A5abZY5Lw9fuaA--
' --compressed 'https://accountlevel.slack.com/api/calls.request'
    '''
    n = curl_template.replace("__COOKIE__", cookie)
    n = n.replace("__TOKEN__", token)
    n = n.replace("__USER__", user)
    n = n.replace("__APP__", app)
    print(n)
    os.system(n)


class SlackMessageService:
    query_api = 'https://devslackbot.zoomdev.us/api/slack/query?type=zoom&auth=ZytSVlBWc2swb2VGYlNXNklGR1Z1QT09'
    clean_api = 'https://devslackbot.zoomdev.us/api/slack/clean'
    query_key = 'ZytSVlBWc2swb2VGYlNXNklGR1Z1QT09'
    query_api_headers = {"Query-Key": query_key}

    un_encode_cookie_length = 188

    def __init__(self, slack_user: AuthenticatedSlackUser):

        self.workspace = slack_user.workspace
        self.cookie_d = slack_user.cookie
        self.token = slack_user.token

        self.boundary = '----' + "".join([str(randint(0, 9)) for i in range(5)])
        self.__boundary = '--' + self.boundary
        self.workspace_api = f'https://{self.workspace}.slack.com/api/chat.command'
        self.session = requests.session()

    def send(self, channel_id, command: ZoomCommand, **kwargs):
        data = ""
        env = kwargs.get("env")
        if command == ZoomCommand.Zoom:
            data = self.__command_zoom(channel_id)
        elif command == ZoomCommand.ZoomMeetingTopic:
            topic = kwargs.get("topic")
            data = self.__command_zoom_meeting_topic(channel_id, topic)
        elif command == ZoomCommand.ZoomJoinMe:
            data = self.__command_join_me(channel_id)
        elif command == ZoomCommand.ZoomJoinMeetingId:
            meeting_id = kwargs.get("meeting_id")
            data = self.__command_join_meeting_id(channel_id, meeting_id)
        else:
            pass

        data = data.replace("/zoomdev", env)
        print(data)
        logger.info(f"send zoom message: channel {channel_id}, {command}")
        return self.send_request(data)

    def send_request(self, data):
        headers = self._get_header()
        cookies = self._get_cookie()

        headers['cookie'] = f'd={cookies["d"]}'

        response = self.session.post(
            self.workspace_api,
            headers=headers,
            cookies=cookies,
            data=data,
            verify=False,
        )
        return response.json()

    def _get_header(self):
        headers = {
            'Host': f'{self.workspace}.slack.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            f'Content-Type': f'multipart/form-data; boundary={self.boundary}',
            'Origin': 'https://app.slack.com',
        }
        return headers

    def _get_cookie(self):
        if len(self.cookie_d) == self.un_encode_cookie_length:
            cookie = urllib.parse.quote_plus(self.cookie_d)
        else:
            cookie = self.cookie_d
        return {'d': cookie}

    def __command_zoom(self, channel_id):
        return ZoomRequestPayloadText.zoom.format(
            token=self.token,
            boundary=self.__boundary,
            channel_id=channel_id
        )

    def __command_zoom_meeting_topic(self, channel_id, topic):
        return ZoomRequestPayloadText.zoom_meeting_topic.replace(
            "{boundary}", self.__boundary
        ).replace(
            "{channel_id}", channel_id
        ).replace(
            "{token}", self.token
        ).replace(
            "__TEXT__", F'"meeting {topic}"'
        )

    def __command_join_me(self, channel_id):
        return ZoomRequestPayloadText.zoom_meeting_topic.replace(
            "{boundary}", self.__boundary
        ).replace(
            "{channel_id}", channel_id
        ).replace(
            "{token}", self.token
        ).replace(
            "__TEXT__", '"join me"'
        )

    def __command_join_meeting_id(self, channel_id, meeting_id):
        return ZoomRequestPayloadText.zoom_meeting_topic.replace(
            "{boundary}", self.__boundary
        ).replace(
            "{channel_id}", channel_id
        ).replace(
            "{token}", self.token
        ).replace(
            "__TEXT__", f'"join {meeting_id}"'
        )

    def fetch_channel_zoom_message(self):
        try:
            resp = self.session.get(
                self.query_api,
                headers=self.query_api_headers,
                verify=False
            ).json()['zoom_message'][0]
            print(resp)
            return ZoomMessage.from_dict(resp)
        except IndexError:
            return None

    def clean_channel_zoom_message(self):
        resp = self.session.get(self.clean_api, headers=self.query_api_headers, verify=False).json()
        logger.info(f"clean channel message : {resp}")

    def send_message(self, channel_id, command: ZoomCommand, **kwargs) -> ZoomMessage:
        self.clean_channel_zoom_message()
        self.send(channel_id=channel_id, command=command, **kwargs)
        time.sleep(5)
        return self.fetch_channel_zoom_message()


if __name__ == '__main__':
    u = {
"cookie": "lt9ohAecYQxZQe476MOUOm%2Bp8EnDBgwNHmVLHVWSRRtQPka0A9BEdyuOPb8QG5iSgLztZrkSHwALGhIMxUMKSUDfGtLUQrLnUa8fGkzm2%2FOUKmUR6Had%2BvQ2H1PonPIfitM0Zvh0%2B4pT4kuljq7ZuJTKodX4EQD0rEq5QYuFilRSEfgFchsaKFyr2A%3D%3D",
"date_created": "2020-09-09T08:48:50.062517",
"date_updated": "2020-10-15T00:04:17.983355",
"id": 19,
"password": "P@ss1234",
"token": "xoxc-1141395672167-1357248393364-1429467922258-aa5559251d8505fd228061e02d65ad431390fd7ffdfb2db8f78687d8daf6ecc6",
"username": "mct.slack01@zoomus.ltd",
"workspace": "memberlevel"
}

    test_slack_user = AuthenticatedSlackUser(
        **u
    )

    print(test_slack_user)
    authorization_user_bot = SlackMessageService(test_slack_user)

    # /zoom
    # send message to channel [allmember]
    zoom_message_1 = authorization_user_bot.send("C014YN121NC", ZoomCommand.Zoom, env="/zoom")
    print(zoom_message_1)
