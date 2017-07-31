#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a Notification
class NOTIF(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'notifs'
    id = Column(Integer, primary_key=True)              # Identifiant unique
    text = Column(String(250))                          # Texte de la notification
    to_push = Column(Boolean)                           # Notification a pousser?
    
    # Any use of linking the notification to the related battle event or cdm ?

    # Constructor
    # Handled by SqlAlchemy, accept keywords names matching the mapped columns, do not override

