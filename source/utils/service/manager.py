#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import falcon
import logging
from utils.resources import health
from utils.resources import login
from utils.resources import replace


class APIServiceManager(falcon.API):
    def __init__(self, config, db):
        super(APIServiceManager, self).__init__()

        logging.info('App will be available on %s' % (config.api.app_path_prefix))

        # Health
        health_resource = health.HealthResource(config, db)

        # Login
        login_resource = login.LoginResource(config, db)

        # Replace word
        replace_resource = replace.ReplaceResource(config, db)

        # Build Routes
        self.add_route(f'{config.api.app_path_prefix}health', health_resource)
        self.add_route(f'{config.api.app_path_prefix}login', login_resource)
        self.add_route(f'{config.api.app_path_prefix}replace', replace_resource)

    def start(self):
        """ A hook to when a Gunicorn worker calls run()."""
        pass

    def stop(self, signal):
        """ A hook to when a Gunicorn worker starts shutting down. """
        pass

