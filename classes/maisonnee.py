#!/usr/bin/env python3
#coding: utf-8

# IMPORTS
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
import modules.globals as sg


# CLASS DEFINITION
class Maisonnee(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, primary_key=True)

    # Associations
    trolls = relationship('Troll', back_populates='maisonnee', primaryjoin='Maisonnee.id == Troll.maisonnee_id')

    # SQL Table Mapping
    __tablename__ = 'maisonnee'

