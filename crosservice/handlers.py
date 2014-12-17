# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import pickle

from gevent.lock import RLock

from crosservice.log import baselogger


class HandlersStorage(object):
    _lock = RLock()
    _data = {}

    def __setitem__(self, key, value):
        self._lock.acquire()
        value = value()
        if key in self._data:
            self._data[key].append(value)
        else:
            self._data[key] = [value]
        self._lock.release()

    def __getitem__(self, item):
        self._lock.acquire()
        if item in self._data:
            data = self._data[item]
        else:
            data = None
        self._lock.release()
        return data

    def __delitem__(self, key):
        self._lock.acquire()
        if key in self._data:
            del self._data[key]
        self._lock.release()

    def __contains__(self, item):
        return item in self._data

    def items(self):
        return self._data.items()


Handlers = HandlersStorage()


class BaseResult(object):
    _status = False
    _error = None
    _result = {}

    def __init__(self, status=None, result=None, error=None):
        if status:
            self._status = status

        if result:
            self._result = result

        if error:
            self._error = error

    def __getattr__(self, item):
        if item in self._result:
            return self._result[item]
        raise AttributeError()

    def __setitem__(self, key, value):
        if self._result:
            self._result[key] = value
        else:
            raise AttributeError('There is no result')

    def __contains__(self, item):
        return item in self._result

    def get_result(self):
        return self._result

    def set_result(self, result):
        self._status = True
        self._result = result

    result = property(get_result, set_result)

    def get_error(self):
        return self._error

    def set_error(self, error):
        self._status = False
        self._error = error

    error = property(get_error, set_error)

    def __nonzero__(self):
        return self._status

    def dump(self):
        return pickle.dumps(self)

    @classmethod
    def load(cls, data):
        return pickle.loads(data)


class Result(BaseResult):
    pass


class HandlerMetaClass(type):
    def __new__(mcs, name, bases, namespace):
        cls = super(HandlerMetaClass, mcs).__new__(mcs, name, bases, namespace)

        if name != 'BaseHandler':
            assert cls.signal, \
                "Signal must be specified at %s" % namespace['__module__']
            if not cls.name:
                cls.name = name

            cls.init()

            Handlers[cls.signal] = cls

        return cls


class BaseHandler(object):
    __metaclass__ = HandlerMetaClass
    signal = None
    name = None

    _logger = None
    _signal = None
    result = None

    def __init__(self):
        self.__name__ = self.name
        self.result = Result()

    @classmethod
    def init(cls):
        cls._logger = baselogger.getChild(cls.name)

    # region logging
    def exception(self, message):
        self._logger.exception(message)

    def critical(self, message):
        self._logger.critical(message)

    def error(self, message):
        self._logger.error(message)

    def warning(self, message):
        self._logger.warning(message)

    def info(self, message):
        self._logger.info(message)

    def debug(self, message):
        self._logger.debug(message)

    # endregion

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)
        return self.result

    def run(self, *args, **kwargs):
        raise NotImplementedError()
