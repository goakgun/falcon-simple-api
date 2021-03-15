#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import falcon
import logging
import jwt
import json
import datetime
from utils.jwt.manager import JWTManager


class LoginResource(object):

    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.application_map_dictionary = self.config.application_map_dictionary
        self.jwt_manager = JWTManager(config, db)

    def on_get(self, req, resp):
        response = {}

        response['error'] = '1'
        response['message'] = '"/login" support POST requests only!'
        resp.status = falcon.HTTP_400
        logging.debug(response)
        resp.body = json.dumps(response, ensure_ascii=False, sort_keys=True, indent=2, separators=(',', ': ')).encode('utf8')



    def on_post(self, req, resp):
        response = {}

        try:
            data = json.loads(req.stream.read())
        except:
            logging.error('Invalid login attempt!')
            data = {}

        # Check required fields are passed
        required_keys = {'user_id', 'password'}
        if data.keys() >= required_keys:
            user_id = data['user_id']
            password = data['password']

            # User Authentication Check
            user_authentication_state = self.jwt_manager.authentication_check(user_id, password)

            if user_authentication_state:
                resp.status = falcon.HTTP_200
                # Create jwt token for user
                response = self.jwt_manager.generate_jwt_token(user_id)
            else:
                resp.status = falcon.HTTP_401
                response = {
                    "error": "1",
                    "message": "Unauthorized Access",
                }

        else:
            resp.status = falcon.HTTP_400
            response = {
                "error": "1",
                "message": "Bad Request",
            }
        resp.body = json.dumps(response, ensure_ascii=False, sort_keys=True, indent=2, separators=(',', ': ')).encode('utf8')
