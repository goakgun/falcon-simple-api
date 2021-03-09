#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import scoping
from utils.db import models


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

    def setup(self):
        # Normally we would add whatever db setup code we needed here.
        # This will for fine for the ORM
        try:
            models.SAModel.metadata.create_all(self.engine)
        except Exception as e:
            logging.error('Could not initialize DB: {}'.format(e))

