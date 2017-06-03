#!/usr/bin/env python
"""
Demo microservice that records player events.
"""
import os
from optparse import OptionParser
from flask import request
from flask_api import FlaskAPI, exceptions
from cassandra.cluster import Cluster
from structures import DynamicActionArray
from util import parse_timesamp, parse_action, cassandra_insert
import settings

parser = OptionParser()
parser.add_option("-p", "--port", dest="port",
                  default=settings.LOCAL_SERVER_PORT,
                  help="Port to listen on", type="int")
parser.add_option("-l", "--listen", dest="listen",
                  default=settings.LOCAL_SERVER_IP,
                  help="Address to listen on", type="string")

# FlaskAPI has an eye candy browser view
app = FlaskAPI(__name__)
data = DynamicActionArray(settings.ACTION_ARRAY_INIT_SIZE,
                          settings.ACTION_GROW_FACTOR,
                          settings.SCORE_VALUES)

# Cassandra startup
if settings.CASSANDRA_SUPPORT:
    cluster = Cluster(settings.CASSANDRA_CLUSTER_IPS)
    session = cluster.connect(settings.CASSANDRA_KEYSPACE)


@app.route('/', methods=['GET'])
def server_status():
    """
    Display server status!
    """
    return {'description': 'Stats Microservice',
            'records': data.length,
            'load': os.getloadavg()}


@app.route('/user/<int:uid>/', methods=['GET', 'POST'])
def user_stats(uid):
    """
    Insert and query user events.
    """
    if request.method == 'POST':
        try:
            timestamp = parse_timesamp(request.data.get('timestamp', ''))
            action = parse_action(request.data.get('action', ''), min_action=1,
                                  max_action=len(settings.SCORE_VALUES))
            data.append(uid, action, timestamp)
            if settings.CASSANDRA_SUPPORT:
                cassandra_insert(session, uid, action, timestamp)
            return {'message': 'ok'}
        except Exception as ex:
            raise exceptions.ParseError(
                detail='{}: {}'.format(ex.__class__.__name__, ex.message))

    if request.method == 'GET':
        try:
            start = parse_timesamp(request.args.get('start', ''))
            end = parse_timesamp(request.args.get('end', ''))
            return data.query(uid, start, end)
        except Exception as ex:
            raise exceptions.ParseError(
                detail='{}: {}'.format(ex.__class__.__name__, ex.message))


if __name__ == '__main__':
    app.debug = settings.LOCAL_SERVER_DEBUG
    (options, args) = parser.parse_args()
    app.run(host=options.listen, port=options.port)
