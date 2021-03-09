#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Libraries Imports
import aumbry
import logging
from gunicorn.app.base import BaseApplication
from gunicorn.workers.sync import SyncWorker

# Projects Imports
from utils.db.manager import DBManager # Database Manager
from utils.log.manager import LogManager
from utils.config.manager import ConfigManager # Config Reader
from utils.service.manager import APIServiceManager # Api Service
from utils.http_server.gateway import CustomWorker, GunicornApp # Custom Gunicorn settings


if __name__ == '__main__':

    # read config file
    config = aumbry.load(
            aumbry.FILE,
            ConfigManager,
            {
                'CONFIG_FILE_PATH': '/opt/api-app/etc/config.yml'
            }
    )

    # Set Log Level and Logging Format
    LogManager(config.api.environment, config.api.log_format)

    # Initialize Database Connection
    db_manager = DBManager(config.db.connection, config.db.pool_recycle)
    db_manager.setup()

    # Initialize API Service
    api_service = APIServiceManager(config, db_manager)
    logging.info('Api Service is started with this configuration: %s' % (config.api))

    # Initialize Gunicorn Http Server Gateway
    gunicorn_app = GunicornApp(api_service, config.gunicorn)
    gunicorn_app.run()
    logging.info('Gunicorn Http App is started with this configuration: %s' % (config.gunicorn))

