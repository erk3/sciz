#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    @hybrid_property
    def last_seen_at(self):
        if all(at is None for at in [self.last_sv2_update_at, self.creation_datetime]): return None
        elif self.last_sv2_update_at is None: return self.creation_datetime
        elif self.creation_datetime is None: return self.last_sv2_update_at
        return max(self.last_sv2_update_at, self.creation_datetime)

    @hybrid_property
    def last_seen_by(self):
        if all(at is None for at in [self.last_sv2_update_by, self.owner_id]): return None
        elif self.last_sv2_update_at is None: return self.owner_id
        elif self.creation_datetime is None: return self.last_sv2_update_by
        else:
            if self.last_sv2_update_at > self.creation_datetime: return self.last_sv2_update_by
            return self.owner_id
