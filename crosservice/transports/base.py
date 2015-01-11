# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import pickle
import socket

from crosservice.handlers import Result
from crosservice.log import baselogger
from crosservice.utils import send_msg, recv_msg


class BaseClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.logger = baselogger.getChild('client')

    def send(self, signal, data):
        log = self.logger.getChild(signal)
        _socket = socket.create_connection((self.host, int(self.port)))
        log.debug("Data: {0}".format(data))
        msg = {'signal': signal, 'data': data}
        msg = pickle.dumps(msg)
        send_msg(_socket, msg)
        response = recv_msg(_socket)
        _socket.close()
        response = Result.load(response)
        if not response:
            log.error(response.error)
        return response


class BaseServer(object):
    pass