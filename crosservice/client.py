# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import bson
import logging
import sys

from gevent import socket

from crosservice.utils import send_msg, recv_msg


log = logging.getLogger(__name__)


class Client(object):
    def __init__(self, host, port):
        self.socket = socket.create_connection((host, int(port)))

    def send(self, action, data):
        log.info("Send action `{0}`".format(action))
        msg = {'action': action, 'data': data}
        msg = bson.BSON().encode(msg)
        send_msg(self.socket, msg)
        response = bson.BSON().decode(recv_msg(self.socket))

        if response['status'] == 'error':
            log.error(response['error'])
        else:
            log.info("OK")
        return response


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        client = Client('127.0.0.1', 1234)
        res = client.send('test', {1: "lol"})
        print(res.get('message'))
        print(res.get('received_data'))