#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.event import Event
from classes.being_troll_private import TrollPrivate
from sqlalchemy import Column, Integer, String, ForeignKey, event
import modules.globals as sg
import re


# CLASS DEFINITION
class userEvent(Event):

    # Constructor is handled by SqlAlchemy do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    # Event type
    type = Column(String(250))
    # Description
    desc = Column(String(150))

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
            self.type = re.sub(r'est\s+', '', self.type)

    def icon(self):
        return 'troll-map-icon.svg'


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(userEvent, 'after_insert')
def upsert_troll_private(mapper, connection, target):
    # Get or create the TrollPrivate
    troll_private = sg.db.session.query(TrollPrivate).get((target.owner_id, target.owner_id))
    if troll_private is None: troll_private = TrollPrivate(troll_id=target.owner_id, viewer_id=target.owner_id)
    # Update it from the userEvent
    if 'depassée' in target.type.lower():
        troll_private.pa = 6
        troll_private.next_dla = target.time
        if troll_private.estimate_dla is not None:
            troll_private.next_dla = troll_private.estimate_dla
    troll_private.last_event_update_at = target.time
    troll_private.last_event_update_by = target.owner_id
    # Upsert it
    sg.db.upsert(troll_private)
