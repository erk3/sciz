#!/usr/bin/env python3
#coding: utf-8

# IMPORTS
from classes.lieu import Lieu
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property


# CLASS DEFINITION
class Piege(Lieu):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('lieu.id', ondelete='CASCADE'), primary_key=True)
    # Creation date
    creation_datetime = Column(DateTime)
    # Type (Glue / Feu)
    piege_type = Column(String(50))
    # MM
    piege_mm = Column(Integer)

    # SQL Table Mapping
    __tablename__ = 'lieu_piege'
    __mapper_args__ = {
        'polymorphic_identity': 'Piège',
        'inherit_condition': id == Lieu.id
    }

    @hybrid_property
    def is_public(self):
        return False
