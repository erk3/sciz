#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a Notification
class EVENT(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)                              # Identifiant unique
    notif = Column(String(250))                                         # Texte de la notification
    notif_to_push = Column(Boolean)                                     # Notification a pousser ?
    type = Column(String(50))                                           # Type d'évènement
    battle_event_id = Column(Integer, ForeignKey('battle_events.id'))   # ID de l'évènement de combat
    cdm_id = Column(Integer, ForeignKey('cdms.id'))                     # ID de l'évènement de CDM
    
    # Associations
    battle_event = relationship("BATTLE_EVENT", back_populates="event")
    cdm = relationship("CDM", back_populates="event")

    # Constructor
    # Handled by SqlAlchemy, accept keywords names matching the mapped columns, do not override

