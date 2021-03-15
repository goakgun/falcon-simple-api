#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from aumbry import Attr, YamlConfig


class DatabaseConfigManager(YamlConfig):

    # Read Environment variables
    database_engine = os.environ.get('DATABASE_ENGINE')
    database_host = os.environ.get('DATABASE_HOST')
    database = os.environ.get('DATABASE')
    database_username = os.environ.get('DATABASE_USERNAME')
    database_password = os.environ.get('DATABASE_PASSWORD')

    # connection_string_formats
    sqlite_connection_string = 'sqlite:////tmp/{}.db'.format(database)
    mysql_connection_string = 'mysql+mysqlconnector://{}:{}@{}:3306/{}'.format(database_username,
            database_password,
            database_host,
            database)
    postgresql_connection_string = 'postgresql://{}:{}@{}:5432/{}'.format(database_username,
            database_password,
            database_host,
            database)


    connection = ''
    pool_recycle = 3600

    if database_engine == 'sqlite':
        connection = sqlite_connection_string
    elif database_engine == 'mysql':
        connection = mysql_connection_string
        pool_recycle = 3600
    elif database_engine == 'postgresql':
        connection = postgresql_connection_string


class GunicornConfigManager(YamlConfig):

    # Read Environment variables
    config = {}
    config['workers'] = int(os.environ.get('GUNICORN_WORKERS'))
    config['timeout'] = int(os.environ.get('GUNICORN_TIMEOUT'))
    config['bind'] = '0.0.0.0:{}'.format(os.environ.get('GUNICORN_BIND_PORT')) 


class ApiConfigManager(YamlConfig):

    # Read Environment variables
    app_path_prefix = os.environ.get('APP_PATH_PREFIX')
    app_environment = os.environ.get('APP_ENVIRONMENT')
    secret_key = os.environ.get('AUTH_SECRET_KEY')
    jwt_expire_limit = int(os.environ.get('AUTH_JWT_EXPIRE_LIMIT')) # in minute
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class ConfigManager(YamlConfig):
    __mapping__ = {
        'db': Attr('db', DatabaseConfigManager),
        'gunicorn': Attr('gunicorn', GunicornConfigManager),
        'api': Attr('api', ApiConfigManager),
        'application_map_dictionary': Attr('application_map_dictionary', dict),
        'application_users': Attr('application_users', dict),
    }

    def __init__(self):
        self.db = DatabaseConfigManager()
        self.api = ApiConfigManager()
        self.gunicorn = GunicornConfigManager()
