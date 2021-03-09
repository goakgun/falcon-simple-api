#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import falcon
import json
import logging
from utils.jwt.manager import JWTManager


def wordReplace(text, mapDict):
    result = " ".join(mapDict.get(item, item) for item in text.split())
    # for key in mapDict:
    #    text = text.replace(key, mapDict[key])
    return result


class ReplaceResource(object):

    def __init__(self, config, db):
        logging.debug(f'Map Dictonary: {config.mapdict}')
        self.mapDict = config.mapdict
        self.jwt_manager = JWTManager(config, db)

    def on_get(self, req, resp):
        response = {}

        # Check jwt token in headers
        if not 'X-AUTH' in req.headers:
            response['error'] = '1'
            response['message'] = 'Error: X-AUTH code is mandatory'
            resp.status = falcon.HTTP_401
        else:
            user_jwt_validation_state, response = self.jwt_manager.validate_jwt_token(req) 

            if user_jwt_validation_state:
                data = json.loads(req.stream.read())
                ''' Check if message parameter is provided '''
                response = {}
                if ('value' not in data):
                    response['error'] = '1'
                    response['message'] = 'Error: value is mandatory'
                    resp.status = falcon.HTTP_501
                else:
                    response['error'] = '0'
                    response['value'] = wordReplace(data['value'], self.mapDict)
                    resp.status = falcon.HTTP_200
        logging.debug(response)
        resp.body = json.dumps(response, ensure_ascii=False, sort_keys=True, indent=2, separators=(',', ': ')).encode('utf8')
