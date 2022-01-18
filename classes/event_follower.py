#!/usr/bin/env python3
#coding: utf-8

# IMPORTS
from classes.event import Event
from classes.being_mob_private import MobPrivate
from sqlalchemy import Column, Integer, String, ForeignKey, event
from sqlalchemy.orm import relationship
import modules.globals as sg


# CLASS DEFINITION
class followerEvent(Event):

    # Constructor is handled by SqlAlchemy do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    # Follower ID
    follower_id = Column(Integer, ForeignKey('being_mob.id'))
    # Follower name
    follower_nom = Column(String(100))
    # Event type
    type = Column(String(250))
    # Description
    desc = Column(String(150))
    # X axis position
    pos_x = Column(Integer)
    # Y axis position
    pos_y = Column(Integer)
    # N axis position
    pos_n = Column(Integer)

    # Associations
    follower = relationship('Mob', primaryjoin='followerEvent.follower_id == Mob.id')
    owner = relationship('Troll', primaryjoin='followerEvent.owner_id == Troll.id', viewonly=True)

    # SQL Table Mapping
    __tablename__ = 'event_follower'
    __mapper_args__ = {
        'polymorphic_identity': 'Suivant',
        'inherit_condition': id == Event.id
    }

    # Additional build logics
    def build(self):
        super().build()
        if hasattr(self, 'type') and self.type is not None and 'ébroue' in self.type:
            self.type = "Ebrouement"
        else:
            self.type = "Arrivée"

    def icon(self):
        return 'follower-map-icon.svg'


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(followerEvent, 'after_insert')
def upsert_mob_private(mapper, connection, target):
    # Get or create the MobPrivate
    mob_private = sg.db.session.query(MobPrivate).get((target.follower_id, target.owner_id))
    if mob_private is None: mob_private = MobPrivate(mob_id=target.follower_id, viewer_id=target.owner_id)
    mob_private.last_event_update_at = target.time
    mob_private.last_event_update_by = target.owner_id
    sg.copy_properties(target, mob_private, ['owner_id', 'pos_x', 'pos_y', 'pos_n'], False)
    sg.db.upsert(mob_private)
