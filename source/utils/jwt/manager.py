#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import jwt
import logging
import datetime
from utils.db import models


class JWTManager(object):
    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.secret_key = config.api.secret_key
        self.algorithm = 'HS256'
        self.jwt_expire_limit = config.api.jwt_expire_limit # minutes
        self.jwt_expire_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=self.jwt_expire_limit) # Set time limit
        return None

    def generate_jwt_token(self, user_id):
        jwt_response = {}
        payload = {"user_id": user_id, "exp":self.jwt_expire_date} # payload

        # Generate jwt token
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm) 

        jwt_response = {
            "error": "0",
            "message": "Succesful",
            "x-auth": token.decode("UTF-8"),
            "Elapse_time": f"{self.jwt_expire_limit}"
        }
        return jwt_response

    def validate_jwt_token(self, req):
        validation = False
        jwt_response = {}

        if 'X-AUTH' in req.headers:
            token = req.headers['X-AUTH'] # Extract token from request header
            try: 
                payload = jwt.decode(token, self.secret_key, self.algorithm)
                validation = True
                logging.debug(f'X-AUTH code {token} validation is succesfully done')
            except jwt.exceptions.ExpiredSignatureError:
                jwt_response = {
                    "error": "1",
                    "message": "X-AUTH code has expired"
                    }
                validation = False
                logging.debug(f'X-AUTH code {token} has expired')
            except:
                jwt_response = {
                    "error": "1",
                    "message": "Invalid X-AUTH code"
                    }
                validation = False
                logging.debug(f'X-AUTH code {token} is invalid')
        else:
            jwt_response = {
                "error": "1",
                "message": "X-AUTH code is required"
                }
            validation = False
            logging.debug(f'X-AUTH code is required!')

        return validation, jwt_response

    def db_health_check(self):
        db_state = models.Users.db_health_check(self.db.session)
        if db_state:
            logging.info(f'Database check passed')
        else:
            logging.error(f'Database check failed')
        return db_state

    def authentication_check(self, user_id, password):
        userObject = models.Users.get_user(self.db.session, user_id, password)
        if userObject:
            authentication = True
            logging.info(f'{user_id} has been succesfully logged in.')
        else:
            authentication = False
            logging.error(f'{user_id} unable to login!')
        return authentication
