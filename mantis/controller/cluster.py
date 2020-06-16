# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong
from flask import jsonify, request, Blueprint

from mantis.config.constant import Auth
from mantis.models.cluster import Cluster
from mantis.models.slack import Slack

cluster_api = Blueprint('cluster', __name__, url_prefix='/qa/cluster')


@cluster_api.route('/', methods=['POST', 'GET'])
def index():
    return jsonify(
        {
            "args": request.args,
            "json": request.json,
            "form": request.form,
        }
    )


@cluster_api.route('/list', methods=['POST', 'GET'])
def list_all():
    all_account = Cluster.query.all()
    return jsonify({"clusters": [slack.serialize_all for slack in all_account]})


@cluster_api.route('/query', methods=['POST', 'GET'])
def query_by():
    team = request.args.get("team")

    cluster_list = Cluster.query.filter_by(
        team=team,
    ).all()

    if not cluster_list:
        return jsonify({"data": "not found"})
    else:
        return jsonify({"slack": [c.serialize_all for c in cluster_api]})


@cluster_api.route('/update', methods=['POST', 'GET'])
def update():
    clusterId = request.form.get("clusterId")
    name = request.form.get("name")
    team = request.form.get("team")

    cluster = Slack.query.get(clusterId)

    if not cluster:
        new_cluster = Cluster()
        new_cluster.name = name
        new_cluster.team = team
        new_cluster.save()
        return jsonify({"create success": new_cluster.serialize_all})
    else:
        cluster.name = name
        cluster.team = team
        cluster.save()

        return jsonify({"update success": cluster.serialize_all})


@cluster_api.route("/add", methods=['POST', 'GET'])
def add():
    name = request.args.get("name")
    team = request.args.get("team")
    creator = request.cookies.get(Auth.USERNAME, "None User")

    try:
        cluster = Cluster(
            name=name,
            team=team,
            creator=creator
        )
        print(cluster)

        cluster.save()
        return jsonify({"clusters": cluster.serialize_all})
    except Exception as e:
        print(e)
        return jsonify({"error": "add account failed"})
