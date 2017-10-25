#!/usr/bin/env python
#-*- coding: utf-8 -*-

###
### /!\ Hooks should only be handled by the webapp /!\
###

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a SCIZ hook
class HOOK(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'hooks'
    id = Column(Integer, primary_key=True)                      # Identifiant unique
    nom = Column(String(50))                                    # Nom du hook
    jwt = Column(String(250))                                   # JWT token sans expiration
    revoked = Column(Boolean())                                 # Révoqué ?
    last_event_id = Column(Integer())                           # ID du dernier évènement traité
    
    # Constructor
    # Handled by SqlAlchemy, accept keywords names matching the mapped columns, do not override
