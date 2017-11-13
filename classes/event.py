#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of an Event (Wrapper for Battle / Piege / CDM) 
class EVENT(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'events'
    __table_args__ = (PrimaryKeyConstraint('id', 'group_id'), )
    # ID unique
    id = Column(Integer, autoincrement=True)
    # Texte de la notification
    notif = Column(String(250))
    # Notification a pousser ?
    notif_to_push = Column(Boolean)
    # Type d'évènement
    type = Column(String(50))
    # ID de l'évènement de combat
    battle_id = Column(Integer, ForeignKey('battles.id'))
    # ID de l'évènement de CDM
    cdm_id = Column(Integer, ForeignKey('cdms.id'))
    # ID de l'évènement de piège
    piege_id = Column(Integer, ForeignKey('pieges.id'))
    # ID du groupe d'appartenance de l'évènement
    group_id = Column(Integer, ForeignKey('groups.id'))
    
    # Associations One-To-One
    battle = relationship("BATTLE", primaryjoin="and_(EVENT.battle_id==BATTLE.id, EVENT.group_id==BATTLE.group_id)", back_populates="event")
    cdm = relationship("CDM", primaryjoin="and_(EVENT.cdm_id==CDM.id, EVENT.group_id==CDM.group_id)", back_populates="event")
    piege = relationship("PIEGE", primaryjoin="and_(EVENT.piege_id==PIEGE.id, EVENT.group_id==PIEGE.group_id)", back_populates="event")
    # Associations One-To-Many
    group = relationship("GROUP", back_populates="events")

    # Constructor is handled by SqlAlchemy, do not override

