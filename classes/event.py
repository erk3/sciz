#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.being_troll import Troll
from sqlalchemy import event, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import re, datetime, os
import modules.globals as sg


# CLASS DEFINITION
class Event(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Owner Troll ID
    owner_id = Column(Integer, ForeignKey('being_troll.id'))
    # Owner Troll name
    owner_nom = Column(String(50))
    # Datetime
    time = Column(DateTime())
    # Type of event (from MH)
    mh_type = Column(String(50))
    # Type of event (from SCIZ)
    sciz_type = Column(String(50))
    # Mail subject
    mail_subject = Column(String(250))
    # Mail body
    mail_body = Column(Text)
    # RM gain
    rm = Column(Integer)
    # MM gain
    mm = Column(Integer)
    # XP gain
    px = Column(Integer)
    # Tiredness loss
    fatigue = Column(Integer)

    # Associations
    owner = relationship('Troll', primaryjoin='Event.owner_id == Troll.id')
    #owner_private_troll = relationship('TrollPrivate', primaryjoin='and_(Event.owner_id == TrollPrivate.troll_id, Event.owner_id = TrollPrivate.viewer_id)')

    # SQL Table Mapping
    __tablename__ = 'event'
    __mapper_args__ = {
        'polymorphic_identity': 'Evénement',
        'polymorphic_on': sciz_type,
    }

    # Additional build logic
    def build(self):
        self.time = datetime.datetime.strptime(self.time, '%d/%m/%Y  %H:%M:%S')

    def icon(self):
        return 'sciz-logo-quarter.png'


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(Event, 'before_insert', propagate=True)
def upsert_event_owner(mapper, connection, target):
    owner_troll = sg.db.session.query(Troll).get(target.owner_id)
    if owner_troll is None:
        troll = Troll(id=target.owner_id, nom=target.owner_nom)
        sg.db.upsert(troll)
    elif target.owner_nom is None:
        target.owner_nom = owner_troll.nom
