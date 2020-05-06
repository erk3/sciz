#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import modules.globals as sg
import datetime


# CLASS DEFINITION
class ChampiPrivate(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Public Tresor ID
    champi_id = Column(Integer, ForeignKey('champi.id', ondelete='CASCADE'))
    # User who has a view on the privates of this champi
    viewer_id = Column(Integer, ForeignKey('being_troll.id', ondelete='CASCADE'))
    # Troll with ownership of the champi
    owner_id = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))
    # Troll who picked it up
    picker_id = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))
    # Freshly picked up at ?
    fraicheur = Column(DateTime)
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
    # Last seen at ?
    last_seen_at = Column(DateTime)
    # Last seen by ?
    last_seen_by = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))
    # Last seen with ?
    last_seen_with = Column(String(50))
    # Last Event update at ?
    last_event_update_at = Column(DateTime)
    # Last Event update by ?
    last_event_update_by = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))
    # Last event update ID ?
    last_event_update_id = Column(Integer, ForeignKey('event.id', ondelete='SET NULL'))
    # Last Reconciliation at ?
    last_reconciliation_at = Column(DateTime)
    # Last Reconciliation by ?
    last_reconciliation_by = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))

    # Associations
    champi = relationship('Champi', back_populates='champi_privates', primaryjoin='ChampiPrivate.champi_id == Champi.id')
    viewer = relationship('Troll', back_populates='viewed_champi_privates', primaryjoin='ChampiPrivate.viewer_id == Troll.id')
    owner = relationship('Troll', back_populates='owned_champi_privates', primaryjoin='ChampiPrivate.owner_id == Troll.id and ChampiPrivate.viewer_id == Troll.id')

    # SQL Table Mapping
    __tablename__ = 'champi_private'
    __table_args__ = (PrimaryKeyConstraint('champi_id', 'viewer_id'), )

    @hybrid_property
    def tooltip(self):
        return '(%s)' % self.champi_id

    def reconciliate(self):
        from classes.user import User
        user = sg.db.session.query(User).get(self.viewer_id)
        if user is not None:
            now = datetime.datetime.now()
            for my_partage in user.partages_actifs:
                # Sharing view
                if my_partage.sharingView:
                    for partage in my_partage.coterie.partages_actifs:
                        champi_private = ChampiPrivate(champi_id=self.champi_id, viewer_id=partage.user_id,
                                                       last_reconciliation_at=now, last_reconciliation_by=self.viewer_id)
                        sg.copy_properties(self, champi_private, ['pos_x', 'pos_y', 'pos_n'], False)
                        sg.db.upsert(champi_private, propagate=False)
                # Sharing Event
                if my_partage.sharingEvents:
                    for partage in my_partage.coterie.partages_actifs:
                        champi_private = ChampiPrivate(champi_id=self.champi_id, viewer_id=partage.user_id,
                                                       last_reconciliation_at=now, last_reconciliation_by=self.viewer_id)
                        sg.copy_properties(self, champi_private, ['owner_id', 'picker_id', 'fraicheur', 'nom', 'qualite',
                                                                    'pos_x', 'pos_y', 'pos_n'], False)
                        sg.db.upsert(champi_private, propagate=False)
