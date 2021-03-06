# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
from .client import Client
from . import constants
from .log import baselogger


class MissedResultError(Exception):
    pass


class BaseSignal(object):
    """
    Base signal's class

    Provides server request, base result validation and logging
    """
    _data = None
    """:type: dict"""
    _host = None
    """:type: str"""
    _port = None
    """:type: int"""
    _result = None
    """:type: handlers.Result"""

    #: Name of signal witch will be requested on server
    signal = None
    """:type: str or unicode"""

    #: List of data fields required in responce
    expect_data = None
    """:type: list or tuple"""

    #: Action on expected data missing
    _missed_data_action = constants.MD_LOG_WARN
    """:type: int"""

    #: Signal's logger
    _log = None
    """:type: logging.Logger"""

    def __init__(self, data=None, _host=None, _port=None, **kwargs):
        """
        :param dict data: request data
        :param str _host: override server's _host
        :param int _port: override server's _port
        """
        if kwargs:
            self._data = kwargs

        if data:
            if kwargs:
                self._data['data'] = data
            else:
                self._data = data

        if _host:
            self._host = _host
        if _port:
            self._port = _port

        self._client = None

    @property
    def log(self):
        if not self._log:
            self._log = baselogger.getChild(self.__class__.__name__)
        return self._log

    @property
    def client(self):
        """
        Create client's instance

        :return: client instance
        :rtype: client.Client
        """
        del self._client
        self._client = Client(self._host, self._port)
        return self._client

    def _send(self):
        """Send request to server"""
        self._result = self.client.send(self.signal, self._data)

    @property
    def result(self):
        """
        Cached result of the request

        :return: request's result
        :rtype: handlers.Result
        """
        if self._result is None:
            self._send()
            if self._result and self.expect_data:
                self._test_missed()
        return self._result

    def _test_missed(self):
        """
        Test for missed fields in the result

        Iterating over each item in `expect_data` and check if it exists
        """
        for expect in self.expect_data:
            if expect not in self._result:
                self._proccess_missed(expect)

    def _proccess_missed(self, expect):
        """
        Run selected action for missed data field

        :param str or unicode expect: missed field name
        """
        if self._missed_data_action == constants.MD_RAISE:
            raise MissedResultError(
                "{0} expected in result, but missed".format(expect)
            )
        elif self._missed_data_action == constants.MD_RESULT_ERR:
            self._result.error = 'Unexpected result, {0} is missed!'.format(
                expect
            )
        elif self._missed_data_action == constants.MD_SET_NONE:
            self._result.expect = None
        else:
            self.log.warning(
                '{0} excpected, but not received!'.format(expect)
            )

    def __del__(self):
        del self._client