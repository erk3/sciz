#!/usr/bin/env python
#-*- coding: utf-8 -*-

###
### /!\ Hooks should only be handled by the webapp /!\
###

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a SCIZ hook
class HOOK(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'hooks'
    __tableargs__ = (UniqueConstraint('name', 'group_id'), )
    # ID unique
    id = Column(Integer, primary_key=True)
    # ID du groupe d'appartenance
    group_id = Column(Integer, ForeignKey('groups.id'))
    # Nom du hook
    name = Column(String(50))
    # JWT token sans expiration
    jwt = Column(String(250))
    # Révoqué ?
    revoked = Column(Boolean())
    # ID du dernier évènement
    last_event_id = Column(Integer())

    # Associations One-To-Many
    group = relationship("GROUP", back_populates="hooks")

    # Constructor is handled by SqlAlchemy, do not override
