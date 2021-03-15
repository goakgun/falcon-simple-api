#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import sha256_crypt

SAModel = declarative_base()

class Users(SAModel):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.String(128), unique=True)
    password = sa.Column(sa.String(256), unique=False)
    email = sa.Column(sa.String(256), unique=True)
    active = sa.Column(sa.Boolean(), nullable=False, default=True)

    def __init__(self, user_id, password, email, active):
        self.user_id = user_id
        self.password = password
        self.email = email
        self.active = active

    @property
    def as_dict(self):
        return {
            'user_id': self.user_id,
            'password': self.password,
            'email': self.email,
            'active': self.active
        }

    def save(self, session):
        with session.begin():
            session.add(self)

    @classmethod
    def db_health_check(cls, session):
        db_health_result = {}
        with session.begin():
            query = session.query(cls)
            try:
                session.execute('SELECT 1')
                db_health_result = True
            except Exception as e:
                logging.error(e)
                db_health_result = False
        return db_health_result

    @classmethod
    def get_user(cls, session, user_id, password):
        userModel = None
        with session.begin():
            query = session.query(cls)
            userModel = query.filter_by(user_id=user_id, active=True).first()

        try:
            # check password
            if not sha256_crypt.verify(password, userModel.password):
                userModel = {}
                logging.error('Invalid login attempt for {user_id}}')
        except:
            logging.error('Invalid login attempt for {user_id}}')
            userModel = None

        return userModel
