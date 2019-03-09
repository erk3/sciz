#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.being import Being
from sqlalchemy import event, inspect, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from classes.being_mob_meta import MetaMob
import modules.globals as sg


# CLASS DEFINITION
class Mob(Being):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('being.id', ondelete='CASCADE'), primary_key=True)
    # Metamob ID
    metamob_id = Column(Integer, ForeignKey('being_mob_meta.id', ondelete='SET NULL'))
    # Tattoo
    tag = Column(String(50))
    # Age
    age = Column(String(50))
    # Race
    race = Column(String(50))
    # Dead ?
    mort = Column(Boolean, default=False)

    # Assosiations
    mob_meta = relationship('MetaMob', back_populates='mobs', primaryjoin='Mob.metamob_id == MetaMob.id')
    mob_privates = relationship('MobPrivate', back_populates='mob', primaryjoin='Mob.id == MobPrivate.mob_id')

    # SQL Table Mapping
    __tablename__ = 'being_mob'
    __mapper_args__ = {
        'polymorphic_identity': 'Monstre',
        'inherit_condition': id == Being.id
    }

    @hybrid_property
    def nom_complet(self):
        if self.tag is not None and self.tag != '':
            return '%s [%s] %s (%d)' % (self.nom, self.age, self.tag, self.id)
        return '%s [%s] (%d)' % (self.nom, self.age, self.id)

    @hybrid_property
    def nom_anonyme(self):
        return '%s [%s]' % (self.nom, self.age)

    @hybrid_property
    def blason_uri(self):
        if self.mob_meta is not None:
            return self.mob_meta.blason_uri
        return None

    @hybrid_property
    def is_follower(self):
        return any(p in self.nom.lower() for p in ['apprivoisé', 'familier', 'golem de cuir', 'golem de métal',
                                                   'golem de mithril', 'golem de papier', 'nâ-hàniym-hééé'])

    @hybrid_property
    def link(self):
        return sg.conf[sg.CONF_MH_SECTION][sg.CONF_LINK_MOB] + str(self.id)


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(Mob, 'before_insert')
@event.listens_for(Mob, 'before_update')
def link_metamob(mapper, connection, target):
    state = inspect(target)
    hist = state.get_history('metamob_id', True)
    if hist.deleted is not None and target.metamob_id is None:
        #  Loop over every metamobs to find the longest one matching the mob name
        metamobs = sg.db.session.query(MetaMob).all()
        len_found_metamob_nom = 0
        for metamob in metamobs:
            len_metamob_nom = len(metamob.nom)
            if metamob.nom in target.nom and len_metamob_nom > len_found_metamob_nom:
                len_found_metamob_nom = len_metamob_nom
                target.metamob_id = metamob.id
                # Get the race if we have a similar mob
                similar_mob = sg.db.session.query(Mob).filter(Mob.metamob_id == target.metamob_id).first()
                if similar_mob is not None and similar_mob:
                    target.race = similar_mob.race
