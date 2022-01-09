#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import modules.globals as sg
import math, datetime


# CLASS DEFINITION
class MobPrivate(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Public Mob ID
    mob_id = Column(Integer, ForeignKey('being_mob.id', ondelete='CASCADE'))
    # Troll who has a view on the privates of this mob
    viewer_id = Column(Integer, ForeignKey('being_troll.id', ondelete='CASCADE'))
    # Troll who own this private mob (Suivant)
    owner_id = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))
    # X axis position
    pos_x = Column(Integer)
    # Y axis position
    pos_y = Column(Integer)
    # N axis position
    pos_n = Column(Integer)
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
    vole = Column(Boolean)
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
    # Last event update at ?
    last_event_update_at = Column(DateTime)
    # Last event update by ?
    last_event_update_by = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))
    # Last event update ID ?
    last_event_update_id = Column(Integer, ForeignKey('event.id', ondelete='SET NULL'))
    # Last seen at ?
    last_seen_at = Column(DateTime)
    # Last seen by ?
    last_seen_by = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))
    # Last seen with ?
    last_seen_with = Column(String(50))
    # Last Reconciliation at ?
    last_reconciliation_at = Column(DateTime)
    # Last Reconciliation by ?
    last_reconciliation_by = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))

    # Associations
    viewer = relationship('Troll', back_populates='viewed_mob_privates', primaryjoin='MobPrivate.viewer_id == Troll.id', viewonly=True)
    owner = relationship('Troll', back_populates='owned_mob_privates', primaryjoin='MobPrivate.owner_id == Troll.id')
    mob = relationship('Mob', back_populates='mob_privates', primaryjoin='MobPrivate.mob_id == Mob.id')

    # SQL Table Mapping
    __tablename__ = 'being_mob_private'
    __table_args__ = (PrimaryKeyConstraint('mob_id', 'viewer_id'), )

    @hybrid_property
    def tooltip(self):
        return '%s (%s) [%s]%s%s' % (self.mob.nom, self.mob_id, self.mob.age,
                                     (' ' + self.mob.tag if self.mob.tag else ''),
                                     (' - ' + self.mob.race if self.mob.race else ''))

    @hybrid_property
    def vie_min(self):
        if self.blessure is None:
            return None
        if self.blessure == 0:
            return self.pdv_min
        elif self.pdv_min is not None:
            return math.floor(self.pdv_min * (100 - min(100, self.blessure + 5)) / 100)
        return None

    @hybrid_property
    def vie_max(self):
        if self.blessure is None:
            return None
        if self.blessure == 0:
            return self.pdv_max
        elif self.pdv_max is not None:
            return math.ceil(self.pdv_max * (100 - max(1, self.blessure - 4)) / 100)
        return None

    @hybrid_property
    def nom_complet(self):
        if self.mob is not None:
            return self.mob.nom_complet
        return None

    def reconciliate(self):
        from classes.user import User
        user = sg.db.session.query(User).get(self.viewer_id)
        if user is not None:
            now = datetime.datetime.now()
            for my_partage in user.partages_actifs:
                # Sharing view
                if my_partage.sharingView:
                    for partage in my_partage.coterie.partages_actifs:
                        mob_private = MobPrivate(mob_id=self.mob_id, viewer_id=partage.user_id,
                                                 last_reconciliation_at=now, last_reconciliation_by=self.viewer_id)
                        sg.copy_properties(self, mob_private, ['pos_x', 'pos_y', 'pos_n'], False)
                        sg.db.upsert(mob_private, propagate=False)
                # Sharing Event
                if my_partage.sharingEvents:
                    for partage in my_partage.coterie.partages_actifs:
                        mob_private = MobPrivate(mob_id=self.mob_id, viewer_id=partage.user_id,
                                                 last_reconciliation_at=now, last_reconciliation_by=self.viewer_id)
                        sg.copy_properties(self, mob_private,
                                           ['owner_id', 'blessure', 'capa_desc', 'capa_effet', 'capa_tour',
                                            'capa_portee',
                                            'nb_att_tour', 'vit_dep', 'vlc',
                                            'vole', 'att_dist', 'att_mag', 'dla', 'sang_froid', 'chargement',
                                            'bonus_malus', 'pos_x', 'pos_y', 'pos_n', 'last_seen_at',
                                            'last_event_at'], False)
                        for attr in ['niv', 'pdv', 'att', 'esq', 'deg', 'reg', 'arm_phy', 'arm_mag', 'vue', 'mm',
                                     'rm',
                                     'tour']:
                            attr_min = attr + '_min'
                            attr_max = attr + '_max'
                            setattr(mob_private, attr_min, sg.do_unless_none(max, (
                            getattr(mob_private, attr_min), getattr(self, attr_min))))
                            setattr(mob_private, attr_max, sg.do_unless_none(min, (
                            getattr(mob_private, attr_max), getattr(self, attr_max))))
                        sg.db.upsert(mob_private, propagate=False)
