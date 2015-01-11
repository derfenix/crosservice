# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import importlib

from log import baselogger


def get_client(transport):
    log = baselogger.getChild('get_client')
    try:
        t = importlib.import_module(
            'crosservice.transports.{0}.client'.format(transport)
        )
    except ImportError:
        log.critical("Import failed")
        return None

    module = getattr(t, 'Client', None)
    log.info("Using {0}".format(module))
    return module