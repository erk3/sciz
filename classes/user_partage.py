#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from sqlalchemy import event, inspect, Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import modules.globals as sg


# CLASS DEFINITION
class Partage(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Identifier of the coterie
    coterie_id = Column(Integer, ForeignKey('coterie.id'))
    # Identifier of the user
    user_id = Column(Integer, ForeignKey('user.id'))
    # Begining of the share, if None then no limit
    start = Column(DateTime, default=None)
    # End of the share, if None then no limit
    end = Column(DateTime, default=None)
    # Admin of the coterie?
    admin = Column(Boolean, default=False)
    # If true, the share is not yet effective
    pending = Column(Boolean, default=False)
    # Is sharing its events?
    sharingEvents = Column(Boolean, default=True)
    # Is sharing its profile?
    sharingProfile = Column(Boolean, default=True)
    # Is sharing its vue?
    sharingView = Column(Boolean, default=True)

    # Associations
    user = relationship('User', back_populates='partages', primaryjoin='Partage.user_id == User.id')
    coterie = relationship('Coterie', back_populates='partages', primaryjoin='Partage.coterie_id == Coterie.id')

    # SQL Table Mapping
    __tablename__ = 'user_partage'


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(Partage, 'before_update')
def do_not_zero_out(mapper, connection, target):
    state = inspect(target)
    for attr in state.attrs:
        hist = state.get_history(attr.key, True)
        if hist.has_changes() and hist.added[0] is None and len(hist.deleted) > 0:
            setattr(target, attr.key, hist.deleted[0])
