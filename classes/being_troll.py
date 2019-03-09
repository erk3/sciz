#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.being import Being
from classes.being_troll_private import TrollPrivate
from sqlalchemy import event, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.ext.hybrid import hybrid_property
import modules.globals as sg


# CLASS DEFINITION
class Troll(Being):

    # Constructor is handled by SqlAlchemy, do not override

    # Identifier
    id = Column(Integer, ForeignKey('being.id', ondelete='CASCADE'), primary_key=True)
    # Race
    race = Column(String(10))
    # Level
    niv = Column(Integer)
    # Kill count
    nb_kill = Column(Integer)
    # Death count
    nb_mort = Column(Integer)
    # Fly count
    nb_mouche = Column(Integer)
    # Guilde identifier
    guilde_id = Column(Integer)
    # Guilde rank identifier
    guilde_rang = Column(Integer)
    # Is in stasis ?
    intangible = Column(Boolean)
    # Is a NPC ?
    pnj = Column(Boolean)
    # Is a friend of the MH team ?
    ami_mh = Column(Boolean)
    # Inscription date
    inscription_date = Column(DateTime)
    # Avatar URI
    blason_uri = Column(String(500))

    # Associations
    user = relationship('User', back_populates='troll', primaryjoin='Troll.id == User.id', uselist=False)
    events = relationship('Event', primaryjoin='Troll.id == Event.owner_id')
    troll_privates = relationship('TrollPrivate', back_populates='troll', primaryjoin='Troll.id == TrollPrivate.troll_id')
    troll_privates_capas = relationship('TrollPrivateCapa', back_populates='troll', primaryjoin='Troll.id == TrollPrivateCapa.troll_id')
    viewed_troll_privates = relationship('TrollPrivate', back_populates='viewer', primaryjoin='Troll.id == TrollPrivate.viewer_id')
    viewed_troll_privates_capas = relationship('TrollPrivateCapa', back_populates='viewer', primaryjoin='Troll.id == TrollPrivateCapa.viewer_id')
    viewed_mob_privates = relationship('MobPrivate', back_populates='viewer', primaryjoin='Troll.id == MobPrivate.viewer_id')
    owned_mob_privates = relationship('MobPrivate', back_populates='owner', primaryjoin='and_(Troll.id == MobPrivate.viewer_id, Troll.id == MobPrivate.owner_id)')
    viewed_tresor_privates = relationship('TresorPrivate', back_populates='viewer', primaryjoin='Troll.id == TresorPrivate.viewer_id')
    owned_tresor_privates = relationship('TresorPrivate', back_populates='owner', primaryjoin='and_(Troll.id == TresorPrivate.viewer_id, Troll.id == TresorPrivate.owner_id)')
    viewed_champi_privates = relationship('ChampiPrivate', back_populates='viewer', primaryjoin='Troll.id == ChampiPrivate.viewer_id')
    owned_champi_privates = relationship('ChampiPrivate', back_populates='owner', primaryjoin='and_(Troll.id == ChampiPrivate.viewer_id, Troll.id == ChampiPrivate.owner_id)')
    owned_lieux = relationship('Lieu', back_populates='owner', primaryjoin='Troll.id == Lieu.owner_id')

    # SQL Table Mapping
    __tablename__ = 'being_troll'
    __mapper_args__ = {
        'polymorphic_identity': 'Trõll',
        'inherit_condition': id == Being.id
    }

    @hybrid_property
    def nom_complet(self):
        return '%s (%d)' % (self.nom, self.id)

    @hybrid_property
    def pseudo(self):
        if self.user is not None and self.user.pseudo is not None:
            return self.user.pseudo
        return self.nom

    @hybrid_property
    def link(self):
        return sg.conf[sg.CONF_MH_SECTION][sg.CONF_LINK_TROLL] + str(self.id)


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(Troll, 'after_insert')
@event.listens_for(Troll, 'after_update')
def create_own_private(mapper, connection, target):
    @event.listens_for(object_session(target), 'after_commit')
    def create_partage_after_commit(session):
        if sg.db.session.query(TrollPrivate).get((target.id, target.id)) is None:
            sg.db.upsert(TrollPrivate(troll_id=target.id, viewer_id=target.id))
