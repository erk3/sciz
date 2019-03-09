#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.tresor_meta import MetaTresor
from sqlalchemy import event, inspect, Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import modules.globals as sg
import datetime


# CLASS DEFINITION
class TresorPrivate(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Public Tresor ID
    tresor_id = Column(Integer, ForeignKey('tresor.id', ondelete='CASCADE'))
    # Trol who has a view on the privates of this tresor
    viewer_id = Column(Integer, ForeignKey('being_troll.id', ondelete='CASCADE'))
    # Troll with ownership of the tresor
    owner_id = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))
    # Metatresor ID
    metatresor_id = Column(Integer, ForeignKey('tresor_meta.id', ondelete='SET NULL'))
    # Type
    nom = Column(String(250))
    # Templates
    templates = Column(String(250))
    # Mithril ?
    mithril = Column(Boolean, default=False)
    # Effect
    effet = Column(String(250))
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
    tresor_meta = relationship('MetaTresor', back_populates='tresor_privates', primaryjoin='TresorPrivate.metatresor_id == MetaTresor.id')
    tresor = relationship('Tresor', back_populates='tresor_privates', primaryjoin='TresorPrivate.tresor_id == Tresor.id')
    viewer = relationship('Troll', back_populates='viewed_tresor_privates', primaryjoin='TresorPrivate.viewer_id == Troll.id')
    owner = relationship('Troll', back_populates='owned_tresor_privates', primaryjoin='TresorPrivate.owner_id == Troll.id and TresorPrivate.viewer_id == Troll.id')

    # SQL Table Mapping
    __tablename__ = 'tresor_private'
    __table_args__ = (PrimaryKeyConstraint('tresor_id', 'viewer_id'), )

    @hybrid_property
    def tooltip(self):
        return '%s (%s)' % (self.tresor.type, self.tresor_id)

    @hybrid_property
    def type(self):
        if self.tresor_meta is not None:
            return self.tresor_meta.type
        return None

    @hybrid_property
    def nom_complet(self):
        return '%s (%d)' % (self.nom, self.tresor_id)

    def reconciliate(self):
        from classes.user import User
        user = sg.db.session.query(User).get(self.viewer_id)
        if user is not None:
            now = datetime.datetime.now()
            session = sg.db.new_session()
            for my_partage in user.partages_actifs:
                if my_partage.user_id != user.id:
                    # Sharing view
                    if my_partage.sharingView:
                        for partage in my_partage.coterie.partages_actifs:
                            tresor_private = TresorPrivate(tresor_id=self.tresor_id, viewer_id=partage.user_id,
                                                           last_reconciliation_at=now,
                                                           last_reconciliation_by=self.viewer_id)
                            sg.copy_properties(self, tresor_private, ['pos_x', 'pos_y', 'pos_n'], False)
                            sg.db.upsert(tresor_private, session, False)
                    # Sharing Event
                    if my_partage.sharingEvents:
                        for partage in my_partage.coterie.partages_actifs:
                            tresor_private = TresorPrivate(tresor_id=self.tresor_id, viewer_id=partage.user_id,
                                                           last_reconciliation_at=now,
                                                           last_reconciliation_by=self.viewer_id)
                            sg.copy_properties(self, tresor_private, ['owner_id', 'metatresor_id', 'nom', 'templates',
                                                                      'mithril', 'effet', 'pos_x', 'pos_y', 'pos_n'],
                                               False)
                            sg.db.upsert(tresor_private, session, False)
            session.commit()
            session.close()


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(TresorPrivate, 'before_insert')
@event.listens_for(TresorPrivate, 'before_update')
def link_metatresor(mapper, connection, target):
    state = inspect(target)
    hist = state.get_history('metatresor_id', True)
    if hist.deleted is not None and target.metatresor_id is None:
        target.metatresor_id, target.nom, target.templates, empty_tresor_type = MetaTresor.link_metatresor(target)
    return target
