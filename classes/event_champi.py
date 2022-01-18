#!/usr/bin/env python3
#coding: utf-8

# IMPORTS
from classes.event import Event
from classes.champi import Champi
from classes.champi_private import ChampiPrivate
from classes.being_troll_private import TrollPrivate
from sqlalchemy import event, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import modules.globals as sg


# CLASS DEFINITION
class champiEvent(Event):

    # Constructor is handled by SqlAlchemy do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    # Champi identifier
    champi_id = Column(Integer, ForeignKey('champi.id'), nullable=False)
    # Event type
    type = Column(String(50), nullable=False)
    # Name
    nom = Column(String(50))
    # Quality
    qualite = Column(String(50))
    # X axis position
    pos_x = Column(Integer)
    # Y axis position
    pos_y = Column(Integer)
    # N axis position
    pos_n = Column(Integer)

    # Associations
    champi = relationship('Champi', primaryjoin='champiEvent.champi_id == Champi.id')

    # SQL Table Mapping
    __tablename__ = 'event_champi'
    __mapper_args__ = {
        'polymorphic_identity': 'Champignon',
        'inherit_condition': id == Event.id
    }

    # Additional build logics
    def build(self):
        super().build()
        if self.type is not None and 'ramassage' in self.type.lower():
            self.type = 'Cueillette'
        if self.type is not None and 'planter' in self.type.lower():
            self.type = 'Jardinage'
            if hasattr(self, 'flag_planter_nok') and self.flag_planter_nok is not None:
                self.type += ' raté (champignon détruit)'
            else:
                self.type += ' réussi'
        if self.nom is None:
            self.nom = 'Champignon Inconnu'

    def icon(self):
        return 'mushroom-map-icon.svg'


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(champiEvent, 'before_insert')
def upsert_targeted_champi(mapper, connection, target):
    champi = Champi(id=target.champi_id)
    sg.db.upsert(champi)


@event.listens_for(champiEvent, 'after_insert')
def upsert_champi_private(mapper, connection, target):
    # Get or create the ChampiPrivate
    champi_private = sg.db.session.query(ChampiPrivate).get((target.champi_id, target.owner_id))
    if champi_private is None: champi_private = ChampiPrivate(champi_id=target.champi_id, viewer_id=target.owner_id)
    # Update the owner if any
    if target.pos_x is None: champi_private.owner_id = target.owner_id
    # Update it from the champiEvent
    sg.copy_properties(target, champi_private, ['nom', 'qualite'], False)
    sg.copy_properties(target, champi_private, ['pos_x', 'pos_y', 'pos_n'], True)
    champi_private.last_event_update_at = target.time
    champi_private.last_event_update_by = target.owner_id
    if target.type == 'Cueillette':
        champi_private.picker_id = target.owner_id
        champi_private.owner_id = target.owner_id
        champi_private.fraicheur = target.time
    # Upsert it
    sg.db.upsert(champi_private)


@event.listens_for(champiEvent, 'before_insert', propagate=True)
def play(mapper, connection, target):
    t = sg.db.session.query(TrollPrivate).get((target.owner_id, target.owner_id))
    if t.pa is None:
        t.pa = 0
    t.pa = max(0, int(t.pa) - 1)
    sg.db.upsert(t)
