#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import falcon
import jwt
import json
import datetime
import logging
from utils.jwt.manager import JWTManager


class HealthResource(object):

    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.mapDict = self.config.mapdict
        self.jwt_manager = JWTManager(config, db)

    def on_get(self, req, resp):
        response = {}

        try:
            data = json.loads(req.stream.read())
        except:
            data = {}

        # Check required fields are passed
        required_keys = {'health-check'}
        if data.keys() >= required_keys:

            # DB Health Check
            db_health_check_state = self.jwt_manager.db_health_check()

            if db_health_check_state:
                resp.status = falcon.HTTP_200
                response = {
                    "error": "0",
                    "message": "Everything seems fine",
                }
            else:
                resp.status = falcon.HTTP_401
                response = {
                    "error": "1",
                    "message": "Unable to connect database",
                }

        else:
            resp.status = falcon.HTTP_400
            response = {
                "error": "1",
                "message": "Bad Request",
            }
        resp.body = json.dumps(response, ensure_ascii=False, sort_keys=True, indent=2, separators=(',', ': ')).encode('utf8')
