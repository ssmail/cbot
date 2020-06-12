# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# author = CarterHong
import datetime
import logging
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

        logger.info(f"send zoom message: channel {channel_id}, {command}")
        return self.send_request(data)

    def send_request(self, data):
        response = self.session.post(
            self.workspace_api,
            headers=self._get_header(),
            cookies=self._get_cookie(),
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
            "__TEXT__", '"join {meeting_id}"'
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
    u = {'id': 7, 'workspace': 'lavglobal', 'username': 'lavender-pox1@grr.la', 'password': 'Slack@123',
         'token': 'xoxc-876060768660-890689517665-1192926057073-a74cecd93c800066fe191db5c65f5bbf80bd8d2534ab1d120c02a58a081d7ee1',
         'cookie': 'CF28SZ0zTFmhaLlwPg4WuH2NT7xPKkTkYO3pPHOfjnGYDO5PeKOe1NnhsDlB5sVsVGzOEHnqDUtKxCcGkAckT3yTrMTcOx0vtl3AjTogEruSfWKvpDXRrua%2FtAtJyh04%2FyfaTjKW8XEQCJ6oRwUILKC%2BkXucJl5F%2BX1g%2BoRsaC3Q%2B6C%2FIdxYZ6kj',
         "date_created": "2020-05-26T06:25:51.681389",
         "date_updated": "2020-06-12T07:18:50.801750",
         }

    test_slack_user = AuthenticatedSlackUser(
        **u
    )

    print(test_slack_user)
    authorization_user_bot = SlackMessageService(test_slack_user)

    # /zoom
    # send message to channel [allmember]
    zoom_message_1 = authorization_user_bot.send("CRDMLKDNW", ZoomCommand.Zoom)
    print(zoom_message_1)
