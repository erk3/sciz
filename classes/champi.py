#!/usr/bin/env python3
#coding: utf-8

# IMPORTS
from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import modules.globals as sg


# CLASS DEFINITION
class Champi(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, primary_key=True)
    # Destroyed ?
    destroyed = Column(Boolean, default=False)

    # Associations
    champi_privates = relationship('ChampiPrivate', back_populates='champi', primaryjoin='Champi.id == ChampiPrivate.champi_id')

    # SQL Table Mapping
    __tablename__ = 'champi'

    @hybrid_property
    def nom(self):
        return 'Champignon Inconnu'

    @hybrid_property
    def link(self):
        return sg.conf[sg.CONF_MH_SECTION][sg.CONF_LINK_TRESOR] + str(self.id)
