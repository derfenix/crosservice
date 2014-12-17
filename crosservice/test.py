# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
# @formatter:off
from gevent import monkey
monkey.patch_all()
# @formatter:on
from crosservice.client import Client
import unittest
from crosservice.handlers import BaseHandler


class TestHandler(BaseHandler):
    name = 'test_handler'
    signal = 'test'

    def run(self, *args, **kwargs):
        self.result.result = kwargs


class TestErrorHandler(BaseHandler):
    signal = 'test_error'

    def run(self, *args, **kwargs):
        self.result.error = kwargs


class MyTestCase(unittest.TestCase):
    def test_success(self):
        client = Client('127.0.0.1', 1234)
        res = client.send('test', {'a': 1})
        self.assertTrue(res)
        self.assertEqual(res.a, 1)
        res.a = 2
        self.assertEqual(res.a, 2)
        self.assertTrue('a' in res)
        self.assertFalse('b' in res)

    def test_error(self):
        client = Client('127.0.0.1', 1234)
        res = client.send('test_error', {'a': 2})
        self.assertFalse(res)
        self.assertEqual(res.error, {'a': 2})
        self.assertRaises(AttributeError, lambda: res.a)

    def test_no_handler(self):
        client = Client('127.0.0.1', 1234)
        res = client.send('signal_not_exists', {'a': 1})
        self.assertFalse(res)
        self.assertIn('signal_not_exists', res.error)
        self.assertRaises(AttributeError, lambda: res.a)



if __name__ == '__main__':
    unittest.main()
