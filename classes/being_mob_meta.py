#!/usr/bin/env python3
#coding: utf-8

# IMPORTS
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import modules.globals as sg


# CLASS DEFINITION
class MetaMob(sg.sqlalchemybase):

    # To pull data from MH, only useful for the name/det and name/avatar association

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, primary_key=True)
    # Name
    nom = Column(String(50))
    # Specifier
    determinant = Column(String(10))
    # Avatar URI
    blason_uri = Column(String(150))
    
    # Associations
    mobs = relationship('Mob', back_populates='mob_meta', primaryjoin='MetaMob.id == Mob.metamob_id')

    # SQL Table Mapping
    __tablename__ = 'being_mob_meta'
