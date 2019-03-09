#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import modules.globals as sg


# CLASS DEFINITION
class MhCall(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy do not override

    # Identifier of the user
    user_id = Column(Integer, ForeignKey('user.id'))
    # Name of the SP called
    nom = Column(String(50))
    # Type of call (dynamic, static...)
    type = Column(String(10))
    # Datetime of the call
    time = Column(DateTime)
    # Status of the call (0 for success, 1-6 for error as defined by MH)
    status = Column(Integer())

    # Associations
    user = relationship('User', back_populates='mh_calls')

    # SQL Table Mapping
    __tablename__ = 'user_mh_call'
    __table_args__ = (PrimaryKeyConstraint('user_id', 'time'), )
