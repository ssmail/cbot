import logging

from flask import jsonify, request, Blueprint

from mantis.common.utils import build_message
from mantis.models.slack import Slack
from mantis.service.slackapi import SlackMessageService, ZoomCommand

slack_api = Blueprint('slack', __name__, url_prefix='/slack')

chat_message = []

keys = ['ZytSVlBWc2swb2VGYlNXNklGR1Z1QT09']

ZOOM_BOT_LIST = ['B0146050FC3', 'B013S9M3N69', 'B01352MV8SJ', 'B012VE561RV', 'B013ESGTREH']


class Token:
    value = ""


class ZoomMessage:
    body = None


zoom_message = ZoomMessage()


@slack_api.route("/")
def alive():
    return "server is running"


@slack_api.route("/message", methods=['GET', 'POST'])
def channel_message():
    logging.info(f"{request.json} \n")
    workspace = request.args.get('workspace', None)

    try:
        zoom_msg = build_message(request.json, workspace)
        logging.info(f"Zoom Msgbox: {zoom_msg}")
        if zoom_msg.botId != "":
            zoom_message.body = zoom_msg
        else:
            logging.info("this is not zoom message")
            chat_message.append(zoom_msg)
    except Exception as e:
        logging.error('add zoom msgbox failed')
        logging.exception(e)
    finally:
        if request.json:
            return request.json
        else:
            return "hello"


def headers():
    d = {}
    for h in request.headers:
        d[h[0]] = h[1]
    return d


@slack_api.route("/command", methods=['GET', 'POST'])
def command():
    return jsonify(
        {
            "cookies": request.cookies,
            "method": request.method,
            "headers": headers(),
            "args": request.args,
            "json": request.json,
            "form": request.form,
        }
    )


@slack_api.route("/query", methods=['GET', 'POST'])
def query():
    key = request.headers.get('Query-Key')
    query_key = request.args.get("auth")
    msg_type = request.args.get("type", "zoom")
    logging.info(f"key: {key}, keys:{keys}")

    if not query_key:
        if key not in keys:
            logging.error(f"bad request: {request.remote_addr}")
            return "bad request"
    elif query_key != "ZytSVlBWc2swb2VGYlNXNklGR1Z1QT09":
        logging.error(f"bad request: {request.remote_addr}")
        return "bad request"

    if msg_type == "zoom":
        return jsonify({"zoomMessage": zoom_message.body})
    elif msg_type == "text":
        return jsonify({"normalMessage": chat_message})
    else:
        logging.error(f"bad request: {request.remote_addr}")
        return "bad request"


@slack_api.route("/clean", methods=['GET', 'POST'])
def clean():
    key = request.headers.get('Query-Key')
    if key not in keys:
        logging.error(f"bad request: {request.remote_addr}")
        return "bad request"

    zoom_message.body = None
    chat_message.clear()

    return jsonify({"zoomMessage": zoom_message.body})


@slack_api.route("/sendMessage", methods=['POST', 'GET'])
def send_message():
    key = request.headers.get('Query-Key')
    if key not in keys:
        logging.error(f"bad request: {request.remote_addr}")
        return "bad request"

    username = request.json.get("slackUser")['username']
    workspace = request.json.get("slackUser")['workspace']
    channel = request.json.get("channel")

    extend = request.json.get("extend")
    command_type = request.json.get("command")

    slack_auth_user: Slack = Slack.query.filter_by(
        username=username,
        workspace=workspace
    ).first()

    if not slack_auth_user:
        return jsonify({"error": "no user"})

    print(command_type)
    print(slack_auth_user.serialize_all)

    slack_bot = SlackMessageService(slack_auth_user)

    if command_type.lower() == "zoom":
        resp = slack_bot.send(channel, ZoomCommand.Zoom)
        return jsonify(resp)
    elif command_type == "ZoomMeetingTopic":
        resp = slack_bot.send(channel, ZoomCommand.ZoomMeetingTopic, topic=extend)
        return jsonify(resp)
    elif command_type == "ZoomJoinMe":
        resp = slack_bot.send(channel, ZoomCommand.ZoomJoinMe, extend=extend)
        return jsonify(resp)
    elif command_type == "ZoomJoinMeeting":
        resp = slack_bot.send(channel, ZoomCommand.ZoomJoinMeetingId, meeting_id=extend)
        return jsonify(resp)
    else:
        return jsonify({"resp": f"error command: {command_type}"})
