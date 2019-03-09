#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import modules.globals as sg


# CLASS DEFINITION
class Lieu(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, primary_key=True)
    # User ID (for privacy of special places like traps)
    owner_id = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))
    # Name
    nom = Column(String(250))
    # Type of place (from SCIZ)
    type = Column(String(50))
    # X axis position
    pos_x = Column(Integer)
    # Y axis position
    pos_y = Column(Integer)
    # N axis position
    pos_n = Column(Integer)
    # Destroyed ?
    destroyed = Column(Boolean, default=False)
    # Last seen at ?
    last_seen_at = Column(DateTime)
    # Last seen by ?
    last_seen_by = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))
    # Last seen with ?
    last_seen_with = Column(String(50))

    # Associations
    owner = relationship('Troll', back_populates='owned_lieux', primaryjoin='Lieu.owner_id == Troll.id')

    # SQL Table Mapping
    __tablename__ = 'lieu'
    __mapper_args__ = {
        'polymorphic_identity': 'Lieu',
        'polymorphic_on': type,
    }

    @hybrid_property
    def tooltip(self):
        return '%s (%s)' % (self.nom, self.id)

    @hybrid_property
    def is_public(self):
        return True

    @hybrid_property
    def is_visible(self):
        return not self.destroyed
