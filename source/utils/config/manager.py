#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aumbry import Attr, YamlConfig


class DatabaseConfigManager(YamlConfig):
    __mapping__ = {
        'connection': Attr('connection', str),
        'pool_recycle': Attr('pool_recycle', int),
    }

    # Default Values for Database Config
    connection = ''
    pool_recycle = 3600

class ApiConfigManager(YamlConfig):
    __mapping__ = {
        'authentication': Attr('authentication', bool),
        'environment': Attr('environment', str),
        'path_prefix': Attr('path_prefix', str),
        'secret_key': Attr('secret_key', str),
        'jwt_expire_limit': Attr('jwt_expire_limit', int),
        'log_format': Attr('log_format', str),
    }

    # Default Values for Api Config
    authentication = True
    environment = 'Test'
    jwt_expire_limit = 20
    path_prefix = '/'
    secret_key = 'super_secret_key'
    log_format = '%(asctime)s - %(message)s'


class ConfigManager(YamlConfig):
    __mapping__ = {
        'db': Attr('db', DatabaseConfigManager),
        'gunicorn': Attr('gunicorn', dict),
        'api': Attr('api', ApiConfigManager),
        'mapdict': Attr('mapdict', dict),
    }

    def __init__(self):
        self.db = DatabaseConfigManager()
        self.api = ApiConfigManager()
        self.gunicorn = {}
