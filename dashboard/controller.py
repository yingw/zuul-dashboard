# -*- coding: utf-8 -*-
import requests

from flask import Blueprint, current_app, render_template, request

from pony.orm import db_session

from dashboard import db
from dashboard.config import config
from dashboard.exceptions import (BadDataFormat, PageOutOfRange, PipeNotFound,
                                  RemoteServerError)
from dashboard.history import BuildSetsHistory, pagination
from dashboard.status import make_queues

status = Blueprint('status', __name__, template_folder='templates')
builds = Blueprint('builds', __name__, template_folder='templates')
error_handlers = Blueprint('error_handlers', __name__,
                           template_folder='templates/errors')


@error_handlers.app_errorhandler(PipeNotFound)
@error_handlers.app_errorhandler(BadDataFormat)
@error_handlers.app_errorhandler(RemoteServerError)
@error_handlers.app_errorhandler(Exception)
def generic_error(error):
    current_app.logger.error(f"{error} on URL: {request.base_url}")
    return render_template('error.html')


@error_handlers.app_errorhandler(PageOutOfRange)
@error_handlers.app_errorhandler(404)
def error_404(error):
    current_app.logger.error(f"{error} on URL: {request.base_url}")
    return render_template('error_404.html')


@status.route('/', methods=['GET'])
@status.route('/status/<string:pipename>', methods=['GET'])
def show_status(pipename=config['DEFAULT']['pipename']):
    url = str(f'{config["ZUUL"]["url"].rstrip("/")}/'
              f'{config["ZUUL"]["status_endpoint"]}')

    res = requests.get(url,
                       timeout=config['DEFAULT'].getfloat('request_timeout'))

    if res.status_code not in [200, 304]:
        current_app.logger.error(res.text)
        raise RemoteServerError('Request for Zuul status failed.')

    res = res.json()
    queues = make_queues(res['pipelines'], pipename)
    return render_template('status.html', queues=queues, pipename=pipename)


@builds.route('/builds')
@builds.route('/builds/<int:page>', methods=['GET'])
@db_session
def show_builds_history(page=1):
    per_page = config['BUILDSET'].getint('per_page')
    pipeline = config['DEFAULT']['pipename']
    page_links = config['BUILDSET'].getint('page_links')
    buildset_log_url = config['BUILDSET']['log_url']

    db.connect()
    buildsets = BuildSetsHistory(pipeline, per_page)
    buildsets.fetch_page(page)

    paginator = pagination(len(buildsets), page, per_page, page_links)

    return render_template('builds_history.html',
                           buildsets=buildsets,
                           paginator=paginator,
                           buildsets_log_url=buildset_log_url)
