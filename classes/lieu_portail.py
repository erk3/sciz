#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.lieu import Lieu
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property


# DEFINITION CLASS
class Portail(Lieu):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('lieu.id', ondelete='CASCADE'), primary_key=True)
    # Creation date
    creation_datetime = Column(DateTime, nullable=False)
    # X axis destination
    pos_x_dst = Column(Integer, nullable=False)
    # Y axis destination
    pos_y_dst = Column(Integer, nullable=False)
    # N axis destination
    pos_n_dst = Column(Integer, nullable=False)
    # X axis dispersion
    pos_x_disp = Column(Integer, nullable=False)
    # Y axis dispersion
    pos_y_disp = Column(Integer, nullable=False)
    # N axis dispersion
    pos_n_disp = Column(Integer, nullable=False)

    # SQL Table Mapping
    __tablename__ = 'lieu_portail'
    __mapper_args__ = {
        'polymorphic_identity': 'Portail',
        'inherit_condition': id == Lieu.id
    }
