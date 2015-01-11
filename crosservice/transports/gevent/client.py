# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
# @formatter:off
from gevent import monkey
monkey.patch_all()
# @formatter:on
from crosservice.transports.base import BaseClient


class Client(BaseClient):
    pass