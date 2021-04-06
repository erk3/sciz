#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.event import Event
from classes.lieu_piege import Piege
from classes.being_troll_private import TrollPrivate
from sqlalchemy import Column, Integer, String, ForeignKey, event, func, and_
from sqlalchemy.orm import relationship
import math
import modules.globals as sg


# CLASS DEFINITION
class cpEvent(Event):

    # Constructor is handled by SqlAlchemy do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    # Trap identifier
    piege_id = Column(Integer, ForeignKey('lieu_piege.id'), nullable=False)
    # Type (Glue / Feu)
    piege_type = Column(String(50))
    # X axis position
    pos_x = Column(Integer)
    # Y axis position
    pos_y = Column(Integer)
    # N axis position
    pos_n = Column(Integer)
    # MM
    piege_mm = Column(Integer)
    # Number of minimum dices for DEG (D3)
    deg_min = Column(Integer)
    # Number of maximum dices for DEG (D3)
    deg_max = Column(Integer)

    # Associations
    piege = relationship('Piege', primaryjoin='cpEvent.piege_id==Piege.id')

    # SQL Table Mapping
    __tablename__ = 'event_cp'
    __mapper_args__ = {
        'polymorphic_identity': 'Construire un Piège',
        'inherit_condition': id == Event.id
    }

    # Additional build logics
    def build(self):
        super().build()

    def icon(self):
        return 'trap.png'


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(cpEvent, 'before_insert')
def play(mapper, connection, target):
    if target.owner_id is not None:
        troll = sg.db.session.query(TrollPrivate).get((target.owner_id, target.owner_id))
        if troll.base_esq_min is not None and troll.base_vue_min is not None:
            target.deg_min = math.trunc((troll.base_vue_min + troll.base_esq_min) / 2)
            target.deg_max = math.trunc((troll.base_vue_max + troll.base_esq_max) / 2)


@event.listens_for(cpEvent, 'before_insert')
def upsert_lieu_piege(mapper, connection, target):
    # Get or create the Trap
    piege = sg.db.session.query(Piege).get(target.piege_id)
    if piege is None:
        piege = Piege(id=target.piege_id, owner_id=target.owner_id, nom='Piège à ' + target.piege_type,
                      creation_datetime=target.time, last_seen_at=target.time, last_seen_by=target.owner_id)
        # Update it from the cpEvent event
        sg.copy_properties(target, piege, ['pos_x', 'pos_y', 'pos_n', 'piege_type', 'piege_mm'], False)
        # Upsert it
        sg.db.upsert(piege)


@event.listens_for(cpEvent, 'after_insert')
def mark_old_piege_destroyed(mapper, connection, target):
    pieges_already_at_pos = sg.db.session.query(Piege).filter(and_(Piege.id != target.piege_id,
                                                                   Piege.pos_x == target.pos_x,
                                                                   Piege.pos_y == target.pos_y,
                                                                   Piege.pos_n == target.pos_n)).all()
    session = sg.db.new_session()
    for piege in pieges_already_at_pos:
        piege.destroyed = True
        sg.db.upsert(piege, session)
    session.commit()
    session.close()


@event.listens_for(cpEvent, 'after_insert')
def upsert_troll_private(mapper, connection, target):
    # Get or create the TrollPrivate
    troll_private = sg.db.session.query(TrollPrivate).get((target.owner_id, target.owner_id))
    if troll_private is None: troll_private = TrollPrivate(troll_id=target.owner_id, viewer_id=target.owner_id)
    # Update it from the tpEvent
    troll_private.pos_x = target.pos_x
    troll_private.pos_y = target.pos_y
    troll_private.pos_n = target.pos_n
    troll_private.last_seen_at = target.time
    troll_private.last_seen_by = target.owner_id
    troll_private.last_seen_with = 'TP'
    troll_private.last_event_update_at = target.time
    troll_private.last_event_update_by = target.owner_id
    # troll_private.last_event_update_id = target.id # FIXME : as it is an autoincrement this is not set already...
    # Upsert it
    sg.db.upsert(troll_private)


@event.listens_for(cpEvent, 'before_insert', propagate=True)
def play(mapper, connection, target):
    t = sg.db.session.query(TrollPrivate).get((target.owner_id, target.owner_id))
    if t.pa is None:
        t.pa = 0
    t.pa = max(0, int(t.pa) - 4)
    sg.db.upsert(t)
