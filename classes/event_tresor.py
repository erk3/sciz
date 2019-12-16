#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.event import Event
from classes.tresor import Tresor
from classes.tresor_meta import MetaTresor
from classes.tresor_private import TresorPrivate
from sqlalchemy import event, func, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import re, modules.globals as sg


# CLASS DEFINITION
class tresorEvent(Event):

    # Constructor is handled by SqlAlchemy do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    # Treasure identifier
    tresor_id = Column(Integer, ForeignKey('tresor.id'), nullable=False)
    # Event type
    type = Column(String(50), nullable=False)
    # Name
    nom = Column(String(250))
    # Tresor type
    tresor_type = Column(String(50))
    # Templates
    templates = Column(String(250))
    # Mithril ?
    mithril = Column(Boolean, default=False)
    # Treasure effect
    effet = Column(String(250))
    # X axis position
    pos_x = Column(Integer)
    # Y axis position
    pos_y = Column(Integer)
    # N axis position
    pos_n = Column(Integer)

    # Associations
    tresor = relationship('Tresor', primaryjoin='tresorEvent.tresor_id == Tresor.id')

    # SQL Table Mapping
    __tablename__ = 'event_tresor'
    __mapper_args__ = {
        'polymorphic_identity': 'Trésor',
        'inherit_condition': id == Event.id
    }

    @hybrid_property
    def str_nom(self):
        return self.nom if self.nom is not None else self.tresor_type

    @hybrid_property
    def str_nom_complet(self):
        nom = self.str_nom
        if self.templates is not None: nom += ' ' + self.templates
        if self.mithril: nom += ' en Mithril'
        return nom

    # Additional build logics
    def build(self):
        super().build()
        # Fix Bidouille
        if self.type == 'Bidouille':
            self.tresor_type = self.type
        # Fix TELEK
        if self.type == 'Télékinésie':
            if any(hasattr(self, attr) and getattr(self, attr) is not None for attr in ['pos_x', 'pos_y']):
                self.type += ' (déplacement)'
            else:
                self.type += ' (ramassage)'
            self.tresor_type = re.sub('Gigots de Gob\'', 'Gigots de Gob', self.tresor_type)
        # Adjust some values
        if self.nom is not None:
            self.nom = re.sub(r'\n', ' ', self.nom).strip()
            if self.nom == 'Malédiction':
                self.nom = 'Mission maudite'
                # FIXME MH : currently no identifier indicated in the mail for cursed mission
                # We fix this by generating one, going backward, hopefully not creating any collision
                self.tresor_id = min(-1, sg.db.session.query(func.min(Tresor.id)).scalar() - 1)
            # Special handling for maps
            res = re.search('((?P<nom>Carte des Raccourcis) : (?P<effet>\w+))(?s)', self.nom)
            if res is not None:
                self.nom = res.groupdict()['nom']
                self.effet = res.groupdict()['effet']
        if self.effet is not None:
            self.effet = re.sub(r'\n', ' ', self.effet).strip()
            if self.effet == '' or self.effet == u'Spécial':
                del self.effet
        if hasattr(self, 'mithril'): self.mithril = self.mithril is not None
        # Update from a metatresor if any matching
        empty_metatresor_id, self.nom, self.templates, self.tresor_type = MetaTresor.link_metatresor(self)


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(tresorEvent, 'before_insert')
def upsert_targeted_tresor(mapper, connection, target):
    tresor = Tresor(id=target.tresor_id, type=target.tresor_type)
    sg.db.upsert(tresor)


@event.listens_for(tresorEvent, 'after_insert')
def upsert_tresor_private(mapper, connection, target):
    # Get or create the TresorPrivate
    tresor_private = sg.db.session.query(TresorPrivate).get((target.tresor_id, target.owner_id))
    if tresor_private is None: tresor_private = TresorPrivate(tresor_id=target.tresor_id, viewer_id=target.owner_id)
    # Update the owner if any
    if target.pos_x is None: tresor_private.owner_id = target.owner_id
    # Update it from the tresorEvent
    sg.copy_properties(target, tresor_private, ['nom', 'templates', 'mithril', 'effet', 'pos_x', 'pos_y', 'pos_n'], False)
    tresor_private.last_event_update_at = target.time
    tresor_private.last_event_update_by = target.owner_id
    # Upsert it
    sg.db.upsert(tresor_private)
