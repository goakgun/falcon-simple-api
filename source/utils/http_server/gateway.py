#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from gunicorn.app.base import BaseApplication
from gunicorn.workers.sync import SyncWorker


''' Custom Gunicorn Worker '''
class CustomWorker(SyncWorker):
    def handle_quit(self, sig, frame):
        self.app.application.stop(sig)
        super(CustomWorker, self).handle_quit(sig, frame)

    def run(self):
        self.app.application.start()
        super(CustomWorker, self).run()


''' Custom Gunicorn App '''
class GunicornApp(BaseApplication):
    """ Custom Gunicorn application
    This allows for us to load gunicorn settings from an external source
    """
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(GunicornApp, self).__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

        self.cfg.set('worker_class', 'utils.http_server.gateway.CustomWorker')

    def load(self):
        return self.application
