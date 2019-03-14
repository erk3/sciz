#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.being_troll_private import TrollPrivate
from classes.event import Event
from classes.lieu_portail import Portail
from sqlalchemy import Column, Integer, ForeignKey, event, and_
from sqlalchemy.orm import relationship
import modules.globals as sg


# CLASS DEFINITION
class tpEvent(Event):

    # Constructor is handled by SqlAlchemy do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    # Portal identifier
    portail_id = Column(Integer, ForeignKey('lieu_portail.id'), nullable=False)
    # X axis position
    pos_x = Column(Integer)
    # Y axis position
    pos_y = Column(Integer)
    # N axis position
    pos_n = Column(Integer)
    # X axis destination
    pos_x_dst = Column(Integer)
    # Y axis destination
    pos_y_dst = Column(Integer)
    # N axis destination
    pos_n_dst = Column(Integer)
    # X axis dispersion
    pos_x_disp = Column(Integer)
    # Y axis dispersion
    pos_y_disp = Column(Integer)
    # N axis dispersion
    pos_n_disp = Column(Integer)

    # Associations
    portail = relationship('Portail', primaryjoin='tpEvent.portail_id==Portail.id')

    # SQL Table Mapping
    __tablename__ = 'event_tp'
    __mapper_args__ = {
        'polymorphic_identity': 'Téléportation',
        'inherit_condition': id == Event.id
    }

    # Additional build logics
    def build(self):
        super().build()


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(tpEvent, 'before_insert')
def upsert_lieu_portail(mapper, connection, target):
    # Get or create the Portail
    portail = sg.db.session.query(Portail).get(target.portail_id)
    if portail is None:
        portail = Portail(id=target.portail_id, owner_id=target.owner_id, nom='Portail de Téléportation',
                          creation_datetime=target.time, last_seen_at=target.time, last_seen_by=target.owner_id)
        # Update it from the tpEvent event
        sg.copy_properties(target, portail,
                           ['pos_x', 'pos_y', 'pos_n', 'pos_x_dst', 'pos_y_dst', 'pos_n_dst', 'pos_x_disp',
                            'pos_y_disp', 'pos_n_disp'],
                           False)
        # Upsert it
        sg.db.upsert(portail)


@event.listens_for(tpEvent, 'after_insert')
def mark_old_portail_destroyed(mapper, connection, target):
    portails_already_at_pos = sg.db.session.query(Portail).filter(and_(Portail.id != target.portail_id,
                                                                       Portail.pos_x == target.pos_x,
                                                                       Portail.pos_y == target.pos_y,
                                                                       Portail.pos_n == target.pos_n)).all()
    session = sg.db.new_session()
    for portail in portails_already_at_pos:
        portail.destroyed = True
        sg.db.upsert(portail, session)
    session.commit()
    session.close()


@event.listens_for(tpEvent, 'after_insert')
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
