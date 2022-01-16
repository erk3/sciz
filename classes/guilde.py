#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import modules.globals as sg


# CLASS DEFINITION
class Guilde(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, primary_key=True)
    # Name
    nom = Column(String(250))
    # Number of members
    count = Column(Integer)

    # Associations
    trolls = relationship('Troll', back_populates='guilde', primaryjoin='Guilde.id == Troll.guilde_id')

    # SQL Table Mapping
    __tablename__ = 'guilde'

