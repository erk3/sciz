#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.event import Event
from classes.being_troll_private import TrollPrivate
from sqlalchemy import Column, Integer, String, ForeignKey, event, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
import modules.globals as sg
import re, datetime


# CLASS DEFINITION
class userEvent(Event):

    # Constructor is handled by SqlAlchemy do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    # Event type
    type = Column(String(250))
    # Description
    desc = Column(String(150))
    # Real life points remaining
    pdv = Column(Integer)
    # Max life points
    pv_max = Column(Integer)
    # Action points remaining
    pa = Column(Integer)
    # Old DLA
    old_dla = Column(DateTime)
    # Next DLA
    next_dla = Column(DateTime)
    # Tiredness
    #fatigue = Column(Integer)

    @hybrid_property
    def str_pdv(self):
        pv_max = self.pv_max if self.pv_max is not None else self.pdv
        return str(self.pdv) + '/' + str(pv_max)

    # SQL Table Mapping
    __tablename__ = 'event_user'
    __mapper_args__ = {
        'polymorphic_identity': 'Utilisateur',
        'inherit_condition': id == Event.id
    }

    # Additional build logics
    def build(self):
        super().build()
        if 'depassée' in self.type.lower():
            self.type = 'DLA dépassée'
        if 'report' in self.type.lower():
            self.type = 'DLA reportée'
        if 'activation' in self.type.lower():
            self.type = 'DLA activée'
        if hasattr(self, 'old_dla') and self.old_dla is not None:
            self.old_dla = datetime.datetime.strptime(self.old_dla, '%d/%m/%Y  %H:%M:%S')
        if hasattr(self, 'next_dla') and self.next_dla is not None:
            self.next_dla = datetime.datetime.strptime(self.next_dla, '%d/%m/%Y  %H:%M:%S')

    def icon(self):
        return 'troll-map-icon.svg'


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(userEvent, 'after_insert')
def upsert_troll_private(mapper, connection, target):
    # Get or create the TrollPrivate
    troll_private = sg.db.session.query(TrollPrivate).get((target.owner_id, target.owner_id))
    if troll_private is None: troll_private = TrollPrivate(troll_id=target.owner_id, viewer_id=target.owner_id)
    # Update it from the userEvent
    troll_private.pa = target.pa
    if 'depassée' in target.type.lower():
        troll_private.next_dla = target.time
        if troll_private.estimate_dla is not None:
            troll_private.next_dla = troll_private.estimate_dla
    else:
        #troll_private.fatigue = target.fatigue
        troll_private.pdv = target.pdv
        troll_private.next_dla = target.next_dla
    troll_private.last_event_update_at = target.time
    troll_private.last_event_update_by = target.owner_id
    # Upsert it
    sg.db.upsert(troll_private)
