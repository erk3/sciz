#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.event import Event
from classes.being_troll import Troll
from classes.being_troll_private import TrollPrivate
from sqlalchemy import Column, Integer, String, ForeignKey, event
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import modules.globals as sg
import math


# CLASS DEFINITION
class aaEvent(Event):

    # Constructor is handled by SqlAlchemy do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    # Public Troll ID (target of the aaEvent)
    troll_id = Column(Integer, ForeignKey('being_troll.id'))
    # Name
    troll_nom = Column(String(50))
    # Level
    niv = Column(Integer)
    # Injury (%)
    blessure = Column(Integer)
    # Minimum life points
    base_pdv_min = Column(Integer)
    # Maximum life points
    base_pdv_max = Column(Integer)
    # Number of minimum dices for ATT (D6)
    base_att_min = Column(Integer)
    # Number of maximum dices for ATT (D6)
    base_att_max = Column(Integer)
    # Number of minimum dices for ESQ (D6)
    base_esq_min = Column(Integer)
    # Number of maximum dices for ESQ (D6)
    base_esq_max = Column(Integer)
    # Number of minimum dices for DEG (D3)
    base_deg_min = Column(Integer)
    # Number of maximum dices for DEG (D3)
    base_deg_max = Column(Integer)
    # Number of minimum dices for REG (D3)
    base_reg_min = Column(Integer)
    # Number of maximum dices for REG (D3)
    base_reg_max = Column(Integer)
    # Number of minimum dices for ARM (D3)
    base_arm_min = Column(Integer)
    # Number of maximum dices for ARM (D3)
    base_arm_max = Column(Integer)
    # Minimum range for VUE
    base_vue_min = Column(Integer)
    # Maximum range for VUE
    base_vue_max = Column(Integer)

    # Associations
    troll = relationship('Troll', primaryjoin='aaEvent.troll_id == Troll.id')
    #troll_private = relationship('TrollPrivate', primaryjoin='and_(aaEvent.troll_id == TrollPrivate.troll_id, aaEvent.owner_id == TrollPrivate.viewer_id)')

    # SQL Table Mapping
    __tablename__ = 'event_aa'
    __mapper_args__ = {
        'polymorphic_identity': 'Analyse Anatomique',
        'inherit_condition': id == Event.id
    }

    @hybrid_property
    def vie_min(self):
        if self.blessure is None or self.blessure == 0:
            return self.pdv_min
        return math.floor(self.pdv_min * (100 - min(100, self.blessure + 5)) / 100)

    @hybrid_property
    def vie_max(self):
        if self.blessure is None or self.blessure == 0:
            return self.pdv_max
        return math.ceil(self.pdv_max * (100 - max(1, self.blessure - 4)) / 100)

    # Additional build logics
    def build(self):
        super().build()
        # aaEvent Niv 1
        for attr in ['pdv', 'att', 'esq', 'deg', 'reg', 'arm', 'vue']:
            setattr(self, 'base_' + attr + '_min', getattr(self, attr + '_min') or getattr(self, attr + '_sup') or getattr(self, attr + '_eq'))
            setattr(self, 'base_' + attr + '_max', getattr(self, attr + '_max') or getattr(self, attr + '_inf') or getattr(self, attr + '_eq'))


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(aaEvent, 'before_insert')
def upsert_targetted_troll(mapper, connection, target):
    troll = Troll(id=target.troll_id, nom=target.troll_nom, niv=target.niv)
    sg.db.upsert(troll)


@event.listens_for(aaEvent, 'after_insert')
def upsert_troll_private(mapper, connection, target):
    # Get or create the TrollPrivate
    troll_private = sg.db.session.query(TrollPrivate).get((target.troll_id, target.owner_id))
    if troll_private is None: troll_private = TrollPrivate(troll_id=target.troll_id, viewer_id=target.owner_id)
    # Update it from the aaEvent
    for attr in ['pdv', 'att', 'esq', 'deg', 'reg', 'arm', 'vue']:
        attr_min = 'base_' + attr + '_min'
        attr_max = 'base_' + attr + '_max'
        setattr(troll_private, attr_min, sg.do_unless_none(max, (getattr(troll_private, attr_min), getattr(target, attr_min))))
        setattr(troll_private, attr_max, sg.do_unless_none(min, (getattr(troll_private, attr_max), getattr(target, attr_max))))
    troll_private.last_event_update_at = target.time
    troll_private.last_event_update_by = target.troll_id
    # Upsert it
    sg.db.upsert(troll_private)
