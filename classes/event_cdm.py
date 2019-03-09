#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.event import Event
from classes.being import Being
from classes.being_mob import Mob
from classes.being_mob_private import MobPrivate
from sqlalchemy import event, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import modules.globals as sg
import re, math


# CLASS DEFINITION
class cdmEvent(Event):

    # Constructor is handled by SqlAlchemy do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    # Public Mob ID (target of the cdmEvent)
    mob_id = Column(Integer, ForeignKey('being_mob.id'))
    # Name
    mob_nom = Column(String(50), nullable=False)
    # Tattoo
    mob_tag = Column(String(50))
    # Age
    mob_age = Column(String(50), nullable=False)
    # Type
    mob_race = Column(String(50))
    # cdmEvent level
    cdm_niv = Column(Integer)
    # Injury (%)
    blessure = Column(Integer)
    # Minimum level
    niv_min = Column(Integer)
    # Maxmimum level
    niv_max = Column(Integer)
    # Minimum life points
    pdv_min = Column(Integer)
    # Maximum life points
    pdv_max = Column(Integer)
    # Number of minimum dices for ATT (D6)
    att_min = Column(Integer)
    # Number of maximum dices for ATT (D6)
    att_max = Column(Integer)
    # Number of minimum dices for ESQ (D6)
    esq_min = Column(Integer)
    # Number of maximum dices for ESQ (D6)
    esq_max = Column(Integer)
    # Number of minimum dices for DEG (D3)
    deg_min = Column(Integer)
    # Number of maximum dices for DEG (D3)
    deg_max = Column(Integer)
    # Number of minimum dices for REG (D3)
    reg_min = Column(Integer)
    # Number of maximum dices for REG (D3)
    reg_max = Column(Integer)
    # Minimum physical ARM
    arm_phy_min = Column(Integer)
    # Maximum physical ARM
    arm_phy_max = Column(Integer)
    # Minimum magical ARM
    arm_mag_min = Column(Integer)
    # Maximum magical ARM
    arm_mag_max = Column(Integer)
    # Minimum range for VUE
    vue_min = Column(Integer)
    # Maximum range for VUE
    vue_max = Column(Integer)
    # Special ability description
    capa_desc = Column(String(150))
    # Special ability effect
    capa_effet = Column(String(150))
    # Special ability duration (T)
    capa_tour = Column(Integer)
    # Special ability range
    capa_portee = Column(String(50))
    # Minimum for MM
    mm_min = Column(Integer)
    # Maximum for MM
    mm_max = Column(Integer)
    # Minimum for RM
    rm_min = Column(Integer)
    # Maximum for RM
    rm_max = Column(Integer)
    # Number of attack each turn
    nb_att_tour = Column(Integer)
    # Move speed
    vit_dep = Column(String(10))
    # VLC ?
    vlc = Column(Boolean)
    # Thief ?
    voleur = Column(Boolean)
    # Ranged attack ?
    att_dist = Column(Boolean)
    # Magick attack ?
    att_mag = Column(Boolean)
    # DLA progression
    dla = Column(String(50))
    # Self control
    sang_froid = Column(String(50))
    # Minimum turn duration
    tour_min = Column(Integer)
    # Maximum turn duration
    tour_max = Column(Integer)
    # Treasures load
    chargement = Column(String(50))
    # Bonus and malus
    bonus_malus = Column(String(150))

    # Associations
    mob = relationship('Mob', primaryjoin='cdmEvent.mob_id == Mob.id')

    # SQL Table Mapping
    __tablename__ = 'event_cdm'
    __mapper_args__ = {
        'polymorphic_identity': 'Connaissance des Monstres',
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
        # Name
        self.mob_nom, self.mob_age, self.mob_tag = Being.parse_name(self.mob_id, self.mob_nom)
        # cdmEvent Niv 1
        attrs = ['niv', 'pdv', 'att', 'esq', 'deg', 'reg', 'arm_phy', 'vue']
        # cdmEvent Niv 2
        if hasattr(self, 'mm_eq'): attrs.append('mm')
        if hasattr(self, 'rm_eq'): attrs.append('rm')
        if self.capa_effet is not None:
            self.capa_effet = re.sub(r'(\n|\|$)', ' ', self.capa_effet)
        self.vlc = sg.parseFrenchBoolean(self.vlc)
        self.att_dist = sg.parseFrenchBoolean(self.att_dist)
        # cdmEvent Niv 3 & 4
        if hasattr(self, 'tour_eq'): attrs.append('tour')
        # cdmEvent Niv 5
        if hasattr(self, 'arm_mag_eq'): attrs.append('arm_mag')
        self.voleur = sg.parseFrenchBoolean(self.voleur)
        self.att_mag = sg.parseFrenchBoolean(self.att_mag)
        # Actual builds
        for attr in attrs:
            setattr(self, attr + '_min', getattr(self, attr + '_min') or getattr(self, attr + '_sup') or getattr(self, attr + '_eq'))
            setattr(self, attr + '_max', getattr(self, attr + '_max') or getattr(self, attr + '_inf') or getattr(self, attr + '_eq'))


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(cdmEvent, 'before_insert')
def upsert_targetted_mob(mapper, connection, target):
    mob = Mob(id=target.mob_id, nom=target.mob_nom, age=target.mob_age, tag=target.mob_tag, race=target.mob_race)
    sg.db.upsert(mob)


@event.listens_for(cdmEvent, 'after_insert')
def upsert_mob_private(mapper, connection, target):
    # Get or create the MobPrivate
    mob_private = sg.db.session.query(MobPrivate).get((target.mob_id, target.owner_id))
    if mob_private is None: mob_private = MobPrivate(mob_id=target.mob_id, viewer_id=target.owner_id)
    # Update it from the cdmEvent
    sg.copy_properties(target, mob_private,
                       ['blessure', 'capa_desc', 'capa_effet', 'capa_tour', 'capa_portee', 'nb_att_tour', 'vit_dep', 'vlc',
                        'voleur', 'att_dist', 'att_mag', 'dla', 'sang_froid', 'chargement', 'bonus_malus'], False)
    for attr in ['niv', 'pdv', 'att', 'esq', 'deg', 'reg', 'arm_phy', 'arm_mag', 'vue', 'mm', 'rm', 'tour']:
        attr_min = attr + '_min'
        attr_max = attr + '_max'
        setattr(mob_private, attr_min, sg.do_unless_none(max, (getattr(mob_private, attr_min), getattr(target, attr_min))))
        setattr(mob_private, attr_max, sg.do_unless_none(min, (getattr(mob_private, attr_max), getattr(target, attr_max))))
    mob_private.last_event_update_at = target.time
    mob_private.last_event_update_by = target.owner_id
    # Upsert it
    sg.db.upsert(mob_private)
