# -*- coding: utf-8 -*-
import unittest
from unittest.mock import MagicMock, patch

from dashboard.db import db
from dashboard.exceptions import PageOutOfRange, RemoteServerError
from dashboard import controller

from tests import fixtures


@patch('dashboard.controller.render_template')
class TestControllerBuildsetHistory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.bind(provider='sqlite', filename=':memory:')
        db.generate_mapping(create_tables=True)

    @classmethod
    def tearDownClass(cls):
        db.disconnect()

    def test_can_invoke_show_build(self, render_template):
        controller.show_builds_history(page=1)

    def test_page_out_of_range_should_raise_exception(self, render_template):
        with self.assertRaises(PageOutOfRange):
            controller.show_builds_history(page=2)

    def test_page_very_out_of_range_should_raise_exception(self, renderer):
        with self.assertRaises(PageOutOfRange):
            controller.show_builds_history(page=2346122865)

    def test_page_negative_should_raise_exception(self, render_template):
        with self.assertRaises(PageOutOfRange):
            controller.show_builds_history(page=-1)

    def test_page_zero_should_raise_exception(self, render_template):
        with self.assertRaises(PageOutOfRange):
            controller.show_builds_history(page=0)


@patch('dashboard.controller.render_template')
@patch('dashboard.controller.current_app')
@patch('dashboard.controller.requests')
class TestControllerStatus(unittest.TestCase):
    def test_can_invoke_show_status(self, requests, *args):
        requests.get = fixtures.status_request()
        controller.show_status('check')

    def test_status_raises_when_cant_download(self, requests, *args):
        result = MagicMock()
        result.status_code = 404
        result.text = "test"
        requests.get = MagicMock(return_value=result)
        with self.assertRaises(RemoteServerError):
            controller.show_status(pipename='check')

    def test_status_raises_when_no_queues(self, requests, *args):
        requests.get = fixtures.status_request(
            filename='tests/static/status_no_queues.json')
        with self.assertRaises(KeyError):
            controller.show_status(pipename='check')
