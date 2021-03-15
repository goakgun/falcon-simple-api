#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import scoping
from utils.db import models
from passlib.hash import sha256_crypt


class DBManager(object):
    def __init__(self, connection=None, pool_recycle=None):
        self.connection = connection
        self.engine = sqlalchemy.create_engine(self.connection, pool_recycle=pool_recycle, pool_pre_ping=True)
        self.DBSession = scoping.scoped_session(
            orm.sessionmaker(
                bind=self.engine,
                autocommit=True
            )
        )
        logging.info('Database connection has been established succesfully.')

    @property
    def session(self):
        return self.DBSession()

    def setup(self, users):
        # Normally we would add whatever db setup code we needed here.
        # This will for fine for the ORM
        try:
            models.SAModel.metadata.create_all(self.engine)
        except Exception as e:
            logging.error('Could not initialize DB: {}'.format(e))
        # Create Application Users

        for user in users:
            hashed_password = sha256_crypt.hash(user['password'])
            user['password'] = hashed_password
            user_exists = self.DBSession.query(models.Users).filter_by(**user).first()
            if not user_exists:
                try:
                    self.DBSession.add(models.Users(**user))
                except Exception as e:
                    logging.error('Could not insert user into DB: {}'.format(e))
