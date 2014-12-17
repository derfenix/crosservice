# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
from crosservice import Client
from crosservice.log import baselogger


MD_LOG_WARN = 0
MD_RAISE = 1
MD_RESULT_ERR = 2


class MissedResultError(Exception):
    pass


class BaseSignal(object):
    signal = None
    _data = None
    _host = None
    _port = None
    _result = None
    """:type: handlers.Result"""
    expect_data = None
    missed_data_error = MD_LOG_WARN
    log = None

    def __init__(self, data, host=None, port=None):
        self._data = data
        if host:
            self._host = host
        if port:
            self._port = port
            
        self.log = baselogger.getChild(self.__class__.__name__)

    @property
    def client(self):
        return Client(self._host, self._port)

    def _send(self):
        self._result = self.client.send(self.signal, self._data)

    @property
    def result(self):
        if self._result is None:
            self._send()
            if self.expect_data:
                self._test_missed()
        return self._result

    def _test_missed(self):
        for expect in self.expect_data:
            if expect not in self._result:
                self._proccess_missed(expect)

    def _proccess_missed(self, expect):
        if self.missed_data_error == MD_RAISE:
            raise MissedResultError(
                "{0} expected in result, but missed".format(expect)
            )
        elif self.missed_data_error == MD_RESULT_ERR:
            self._result.error = 'Unexpected result, {0} is missed!'.format(
                expect
            )
        else:
            self.log.warning(
                '{0} excpected, but not received!'.format(expect)
            )