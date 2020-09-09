import datetime
import json

from flask import jsonify, request, Blueprint

from mantis.models.epic import Epic

epic_api = Blueprint('epic', __name__, url_prefix='/qa/epic')


@epic_api.route('/go', methods=['POST', 'GET'])
def index():
    meeting_id = request.args.get('ZoomMeetingId')
    d = request.args.to_dict()
    d['time'] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    value = json.dumps(d)
    print(value)
    epic = Epic(zoomMeetingId=meeting_id, value=value, cluster='go')
    epic.save()
    print('--------------------------')
    print(epic.serialize_all)
    print('--------------------------')
    return jsonify({'meeting_id': epic.serialize_all})


@epic_api.route('/query', methods=['POST', 'GET'])
def query():
    meeting_id = request.args.get('ZoomMeetingId')
    epic_list = Epic.query.filter(Epic.zoomMeetingId == meeting_id).order_by(Epic.date_created).all()
    l = []
    for i in epic_list:
        l.append(json.loads(i.value))
    return jsonify({'meeting_id': meeting_id, "list": l})
