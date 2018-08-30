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
    # Date de la notification
    time = Column(DateTime())
    # Notification
    notif = Column(String(500))
    # Notification masquée ?
    hidden = Column(Boolean)
    # Type d'évènement
    type = Column(String(50))
    # ID de l'évènement de combat
    battle_id = Column(Integer, ForeignKey('battles.id', ondelete="CASCADE"))
    # ID de l'évènement de CDM
    cdm_id = Column(Integer, ForeignKey('cdms.id', ondelete="CASCADE"))
    # ID de l'évènement de AA
    aa_id = Column(Integer, ForeignKey('aas.id', ondelete="CASCADE"))
    # ID de l'évènement de piège
    piege_id = Column(Integer, ForeignKey('pieges.id', ondelete="CASCADE"))
    # ID de l'évènement de portail
    portal_id = Column(Integer, ForeignKey('portals.id', ondelete="CASCADE"))
    # ID de l'évènement d'identification des champignons
    idc_id = Column(Integer, ForeignKey('idcs.id', ondelete="CASCADE"))
    # ID de l'évènement d'identification des trésors
    idt_id = Column(Integer, ForeignKey('idts.id', ondelete="CASCADE"))
    # ID du groupe d'appartenance de l'évènement
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    
    # Associations One-To-One
    battle = relationship("BATTLE", primaryjoin="and_(EVENT.battle_id==BATTLE.id, EVENT.group_id==BATTLE.group_id)", back_populates="event")
    cdm = relationship("CDM", primaryjoin="and_(EVENT.cdm_id==CDM.id, EVENT.group_id==CDM.group_id)", back_populates="event")
    aa = relationship("AA", primaryjoin="and_(EVENT.aa_id==AA.id, EVENT.group_id==AA.group_id)", back_populates="event")
    piege = relationship("PIEGE", primaryjoin="and_(EVENT.piege_id==PIEGE.id, EVENT.group_id==PIEGE.group_id)", back_populates="event")
    portal = relationship("PORTAL", primaryjoin="and_(EVENT.portal_id==PORTAL.id, EVENT.group_id==PORTAL.group_id)", back_populates="event")
    idc = relationship("IDC", primaryjoin="and_(EVENT.idc_id==IDC.id, EVENT.group_id==IDC.group_id)", back_populates="event")
    idt = relationship("IDT", primaryjoin="and_(EVENT.idt_id==IDT.id, EVENT.group_id==IDT.group_id)", back_populates="event")
    # Associations One-To-Many
    group = relationship("GROUP", back_populates="events")

    # Constructor is handled by SqlAlchemy, do not override

    # Get the actual notification associated to this event
    def getNotif(self, short):
        notif = ''
        obj = None
        obj = self.battle if self.battle_id is not None else obj
        obj = self.cdm if self.cdm_id is not None else obj
        obj = self.aa if self.aa_id is not None else obj
        obj = self.piege if self.piege_id is not None else obj
        obj = self.portal if self.portal_id is not None else obj
        obj = self.idc if self.idc_id is not None else obj
        obj = self.idt if self.idt_id is not None else obj
        return sg.pretty_print(obj, short)
