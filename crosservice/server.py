# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
# @formatter:off
import pickle
from gevent import monkey
monkey.patch_all()
# @formatter:on
from crosservice.handlers import Handlers, Result
import logging

from gevent.server import StreamServer

from crosservice.utils import recv_msg, send_msg

# noinspection PyUnresolvedReferences
import test


log = logging.getLogger(__name__)


def handler(socket, address):
    message = recv_msg(socket)
    message = pickle.loads(message)
    res = Result()

    # Check for all required keys
    if not ('data' in message and 'action' in message):
        log.error("Incomplete message, passed: {0}".format(message.keys()))
        res.error = 'Missed data or action'

        send_msg(socket, res)
        return

    action = message['action']
    data = message['data']

    # Trying to execute action's handler
    if action in Handlers:
        handlers = Handlers[action]
        for h in handlers:
            """:type: crosservice.handlers.Handler"""
            log.info("Using `{0}` as handler for action `{1}`".format(h,
                                                                      action))
            res = h(**data)
    else:
        log.warning("No handler for action `{0}`".format(action))
        res.error = "No handler for action {0}".format(action)

    send_msg(socket, res)


def start_server(host, port, spawn):
    log.info(
        "Start listening at {host}:{port} with spawn value {spawn}".format(
            host=host, port=port, spawn=spawn
        ))
    server = StreamServer((host, int(port)), handle=handler, spawn=spawn)
    server.serve_forever()
