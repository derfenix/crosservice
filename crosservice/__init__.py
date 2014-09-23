# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import logging
from crosservice.client import Client
from crosservice.server import start_server
from crosservice.signals import register as register_signal

logging.basicConfig(level=logging.DEBUG)