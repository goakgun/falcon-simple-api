#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


class LogManager(object):
    def __init__(self, environment, log_format):
        self.environment = environment
        self.log_format = log_format
        if environment == 'Test':
            log_level = 'DEBUG'
            logging.basicConfig(level=logging.DEBUG, format=log_format)
        elif environment == 'Staging':
            log_level = 'INFO'
            logging.basicConfig(level=logging.INFO, format=log_format)
        elif environment == 'Prod':
            log_level = 'WARNING'
            logging.basicConfig(level=logging.WARNING, format=log_format)

        logging.warning(f'App is running on {self.environment} environment')
        logging.warning(f'Log Level is set to {log_level}')
