# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
# @formatter:off
from gevent import monkey
monkey.patch_all()
# @formatter:on
import bson
import logging

from gevent.server import StreamServer

from crosservice.signals import SIGNALS, register, Signal

from crosservice.utils import recv_msg, send_msg


log = logging.getLogger(__name__)


def handler(socket, address):
    message = recv_msg(socket)

    # Trying to load data from received json message
    try:
        message = bson.BSON().decode(message)
    except ValueError:
        log.error("Bad message format")
        msg = {
            'status': 'error', 'message': 'Bad message format'
        }
        msg = bson.BSON().decode(msg)
        send_msg(socket, msg)
        return

    # Check for all required keys
    if not ('data' in message and 'action' in message):
        log.error("No data or action in message")
        msg = {
            'status': 'error', 'message': 'Missed data or action'
        }
        msg = bson.BSON().decode(msg)
        send_msg(socket, msg)
        return

    action = message['action']
    data = message['data']

    # Trying to execute action's handler
    if action in SIGNALS and isinstance(SIGNALS[action], Signal):
        h = SIGNALS[action]
        """:type: crosservice.signals.Signal"""
        log.info("Using `{0}` as handler for action `{1}`".format(h, action))
        msg = h(data)
    else:
        log.warning("No handler for action `{0}`".format(action))
        msg = {"error": "No signal for action {0}".format(action), "status": "error"}

    msg = bson.BSON().encode(msg)
    send_msg(socket, msg)


def start_server(host, port, spawn):
    log.info("Start listening at {host}:{port} with spawn value {spawn}".format(
        host=host, port=port, spawn=spawn
    ))
    server = StreamServer((host, int(port)), handle=handler, spawn=spawn)
    server.serve_forever()


# Test handler
def test(data):
    return {
        'status': 'ok',
        'message': 'Test passed',
        'received_data': data
    }


register('test', test)