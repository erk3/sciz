#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import modules.globals as sg


# CLASS DEFINITION
class Tresor(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, primary_key=True)
    # Type
    type = Column(String(50))

    # Associations
    tresor_privates = relationship('TresorPrivate', back_populates='tresor', primaryjoin='Tresor.id == TresorPrivate.tresor_id')

    # SQL Table Mapping
    __tablename__ = 'tresor'

    @hybrid_property
    def link(self):
        return sg.conf[sg.CONF_MH_SECTION][sg.CONF_LINK_TRESOR] + str(self.id)
