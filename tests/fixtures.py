# -*- coding: utf-8 -*-
import json
import random
from unittest.mock import MagicMock

from dashboard.config import config
from dashboard.status import Buildset, Job, TimeTracker


def time_tracker():
    return TimeTracker(start=random.randint(1000, 100000),  # noqa
                       elapsed=random.randint(1000, 100000),  # noqa
                       remaining=random.randint(1000, 100000),  # noqa
                       estimated=random.randint(1000, 100000))  # noqa


def job():
    return Job(name="test_name", result="test_result",
               url="http://fake_url", report_url="http://fake_url",
               canceled=False, voting=False, retry=False,
               worker={"name": "fake_name"},
               time_tracker=TimeTracker(start=random.randint(1000, 100000),  # noqa
                                        elapsed=random.randint(1000, 100000),  # noqa
                                        remaining=random.randint(1000, 100000),  # noqa
                                        estimated=random.randint(1000, 100000)))  # noqa


def buildset():
    return Buildset(name="test_name", buildset_id="12345,6", jobs=[],
                    enqueue_time=random.randint(1000, 100000),  # noqa
                    owner={'name': 'John smith'}, ref='12345',
                    review_url="http://fake_url")


def status_request(filename=None, status_code=200):
    result = MagicMock()
    result.status_code = status_code
    filename = filename or config['DEFAULT']['status_endpoint']
    with open(filename) as json_data:
        result.json = MagicMock(return_value=json.load(json_data))
    return MagicMock(return_value=result)
