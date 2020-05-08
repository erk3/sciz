#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from sqlalchemy import event, Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import modules.globals as sg
import datetime, math


# CLASS DEFINITION
class TrollPrivate(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Public Troll ID
    troll_id = Column(Integer, ForeignKey('being_troll.id', ondelete='CASCADE'))
    # Troll who has a view on the privates of this troll
    viewer_id = Column(Integer, ForeignKey('being_troll.id', ondelete='CASCADE'))
    # Total investment points
    pi = Column(Integer)
    # Available investment points
    pi_disp = Column(Integer)
    # X axis position
    pos_x = Column(Integer)
    # Y axis position
    pos_y = Column(Integer)
    # N axis position
    pos_n = Column(Integer)
    # Injury (%)
    blessure = Column(Integer)
    # Real life points remaining
    pdv = Column(Integer)
    # Minimum life point base (without bonus)
    base_pdv_min = Column(Integer)
    # Maximum life point base (without bonus)
    base_pdv_max = Column(Integer)
    # Physical life points bonus
    bonus_pdv_phy = Column(Integer)
    # Magical life points bonus
    bonus_pdv_mag = Column(Integer)
    # Action points remaining
    pa = Column(Integer)
    # Next DLA
    next_dla = Column(DateTime)
    # Number of minimum dices for ATT (D6)
    base_att_min = Column(Integer)
    # Number of maximum dices for ATT (D6)
    base_att_max = Column(Integer)
    # Physical bonus for ATT
    bonus_att_phy = Column(Integer)
    # Magical bonus for ATT
    bonus_att_mag = Column(Integer)
    # Number of minimum dices for ESQ (D6)
    base_esq_min = Column(Integer)
    # Number of maximum dices for ESQ (D6)
    base_esq_max = Column(Integer)
    # Physical bonus for ESQ
    bonus_esq_phy = Column(Integer)
    # Magical bonus for ESQ
    bonus_esq_mag = Column(Integer)
    # Number of minimum dices for DEG (D3)
    base_deg_min = Column(Integer)
    # Number of maximum dices for DEG (D3)
    base_deg_max = Column(Integer)
    # Physical bonus for DEG
    bonus_deg_phy = Column(Integer)
    # Magical bonus for DEG
    bonus_deg_mag = Column(Integer)
    # Number of minimum dices for REG (D3)
    base_reg_min = Column(Integer)
    # Number of maximum dices for REG (D3)
    base_reg_max = Column(Integer)
    # Physical bonus for REG
    bonus_reg_phy = Column(Integer)
    # Magical bonus for REG
    bonus_reg_mag = Column(Integer)
    # Minimum range for VUE
    base_vue_min = Column(Integer)
    # Maximum range for VUE
    base_vue_max = Column(Integer)
    # Physical bonus for VUE
    bonus_vue_phy = Column(Integer)
    # Magical bonus for VUE
    bonus_vue_mag = Column(Integer)
    # Number of minimum dices for ARM (D3)
    base_arm_min = Column(Integer)
    # Number of maximum dices for ARM (D3)
    base_arm_max = Column(Integer)
    # Number of malus dices substracted for ARM (D3)
    malus_arm = Column(Integer)
    # Physical bonus for ARMP (from inventory)
    bonus_arm_phy = Column(Integer)
    # Magical bonus for ARMP (from inventory, buffs and flies)
    bonus_arm_mag = Column(Integer)
    # Minimum for MM
    base_mm_min = Column(Integer)
    # Maximum for MM
    base_mm_max = Column(Integer)
    # Physical bonus for MM
    bonus_mm_phy = Column(Integer)
    # Magical bonus for MM
    bonus_mm_mag = Column(Integer)
    # Minimum for RM
    base_rm_min = Column(Integer)
    # Maximum for RM
    base_rm_max = Column(Integer)
    # Physical bonus for RM
    bonus_rm_phy = Column(Integer)
    # Magical bonus for RM
    bonus_rm_mag = Column(Integer)
    # Tiredness
    fatigue = Column(Integer)
    # Camouflaged ?
    camouflage = Column(Boolean)
    # Invisible ?
    invisible = Column(Boolean)
    # Immobilized ?
    immobile = Column(Boolean)
    # On the ground ?
    terre = Column(Boolean)
    # Running ?
    course = Column(Boolean)
    # Levitating ?
    levite = Column(Boolean)
    # Attack suffered counter
    nb_att_sub = Column(Integer)
    # Programmed parry counter
    nb_parade_prog = Column(Integer)
    # Programmed counter-attack counter
    nb_ctr_att_prog = Column(Integer)
    # Programmed retreat counter
    nb_retraite_prog = Column(Integer)
    # Programmed retreat directions (chronological order)
    dir_retraite_prog = Column(String(50))
    # Minimum turn duration (minutes)
    base_tour_min = Column(Integer)
    # Maximum turn duration (minutes)
    base_tour_max = Column(Integer)
    # Physical bonus for turn duration
    bonus_tour_phy = Column(Integer)
    # Magical bonus for turn duration
    bonus_tour_mag = Column(Integer)
    # Physical malus for turn duration (inventory weight)
    malus_poids_phy = Column(Integer)
    # Magical malus for turn duration
    malus_poids_mag = Column(Integer)
    # Concentration (%)
    base_concentration = Column(Integer)
    # Physical bonus for CON (%)
    bonus_concentration_phy = Column(Integer)
    # Magical bonus for CON %
    bonus_concentration_mag = Column(Integer)
    # Last event update at ?
    last_event_update_at = Column(DateTime)
    # Last event update by ?
    last_event_update_by = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))
    # Last event update ID ?
    last_event_update_id = Column(Integer, ForeignKey('event.id', ondelete='SET NULL'))
    # Last SP4 update at ?
    last_sp4_update_at = Column(DateTime)
    # Last SP4 update by ?
    last_sp4_update_by = Column(Integer, ForeignKey('being_troll.id', ondelete='SET NULL'))
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
    troll = relationship('Troll', back_populates='troll_privates', primaryjoin='TrollPrivate.troll_id == Troll.id')
    viewer = relationship('Troll', back_populates='viewed_troll_privates', primaryjoin='TrollPrivate.viewer_id == Troll.id')
    troll_privates_capas = relationship('TrollPrivateCapa', primaryjoin='and_(TrollPrivate.troll_id == foreign(TrollPrivateCapa.troll_id), TrollPrivate.viewer_id == foreign(TrollPrivateCapa.viewer_id))')

    # SQL Table Mapping
    __tablename__ = 'being_troll_private'
    __table_args__ = (PrimaryKeyConstraint('troll_id', 'viewer_id'), )

    @hybrid_property
    def tooltip(self):
        return '%s (%s) - %s N%s' % (self.troll.nom, self.troll_id, self.troll.race, self.troll.niv)

    @hybrid_property
    def portee(self):
        if all(x is not None for x in [self.base_vue_max, self.bonus_vue_phy, self.bonus_vue_mag]):
            return self.base_vue_max + self.bonus_vue_phy + self.bonus_vue_mag
        return None

    @hybrid_property
    def pdv_max(self):
        if self.last_sp4_update_at is not None:
            # Here _min attrs and _max attrs are supposed to be equal
            return self.base_pdv_min + self.bonus_pdv_phy + self.bonus_pdv_mag
        return None

    @hybrid_property
    def malus_blessure(self):
        if self.last_sp4_update_at is not None:
            return (250 * (self.pdv_max - self.pdv)) // self.pdv_max
        return None

    @hybrid_property
    def tour(self):
        if self.last_sp4_update_at is not None:
            # Here _min attrs and _max attrs are supposed to be equal, pdv is also supposed to be set
            mins = self.base_tour_min
            # Add stuff weight
            mins += self.malus_poids_phy + self.malus_poids_mag
            # Add wound malus
            mins += self.malus_blessure
            # Add bonuses (templates, flies, etc.)
            mins += self.bonus_tour_phy + self.bonus_tour_mag
            # Keep the result at minimum base tour
            return max(self.base_tour_min, mins)
        return None

    @hybrid_property
    def estimate_dla(self):
        if self.last_sp4_update_at is not None:
            # Here the hybrid property is supposed to work
            return self.next_dla + datetime.timedelta(minutes=self.tour)
        return None

    @hybrid_property
    def str_fatigue(self):
        if self.fatigue is not None:
            res = None
            if self.fatigue <= 0: res = 'Parfaitement reposé'
            if self.fatigue >= 1 and self.fatigue < 3: res = 'En pleine forme'
            if self.fatigue >= 3 and self.fatigue < 5: res = 'Tonique'
            if self.fatigue >= 5 and self.fatigue < 7: res = 'Juste Bien'
            if self.fatigue >= 7 and self.fatigue < 11: res = 'Plus très frais'
            if self.fatigue >= 11 and self.fatigue < 16: res = 'Mou du genou'
            if self.fatigue >= 16 and self.fatigue < 21: res = 'Fatigué'
            if self.fatigue >= 21 and self.fatigue < 31: res = 'Crevé'
            if self.fatigue >= 31 and self.fatigue < 41: res = 'Lessivé'
            if self.fatigue >= 41: res = 'Complètement épuisé'
            return '%s (%s)' % (res, self.fatigue)
        return None

    @hybrid_property
    def actions(self):
        actions = ''
        if self.nb_parade_prog is not None and self.nb_parade_prog > 0: actions += 'Parade x' + str(self.nb_parade_prog) + ' | '
        if self.nb_ctr_att_prog is not None and self.nb_ctr_att_prog > 0: actions += 'Contre-Attaque x' + str(self.nb_ctr_att_prog) + ' | '
        if self.nb_retraite_prog is not None and self.nb_retraite_prog > 0: actions += 'Retraite x' + str(self.nb_retraite_prog) + ' ( ' + self.dir_retraite_prog + ') | '
        if len(actions) > 3: actions = actions[:-3]
        return actions

    @hybrid_property
    def statut(self):
        statut = ''
        if self.troll.intangible: statut += 'Intangible | '
        if self.immobile: statut += 'Immobilisé | '
        if self.camouflage: statut += 'Camouflé | '
        if self.course: statut += 'En course | '
        if self.invisible: statut += 'Invisible | '
        if self.levite: statut += 'Lévite | '
        if self.terre: statut += 'A terre | '
        if len(statut) > 3: statut = statut[:-3]
        return statut

    @hybrid_property
    def corpulence(self):
        if self.last_sp4_update_at is not None:
            return math.floor(self.pdv_max / 10) + self.bonus_arm_phy
        return None

    @hybrid_property
    def agilite(self):
        if self.last_sp4_update_at is not None:
            return self.base_esq_min + self.base_reg_min
        return None

    @hybrid_property
    def reflexe_stabilite(self):
        agilite = self.agilite
        if agilite is not None:
            return math.floor((agilite / 3) * 2)
        return None

    @hybrid_property
    def vie_min(self):
        if self.pdv is not None:
            return self.pdv
        elif self.blessure is None or self.blessure == 0:
            return self.base_pdv_min
        elif self.base_pdv_min is not None:
            return math.floor(self.base_pdv_min * (100 - min(100, self.blessure + 5)) / 100)
        return None

    @hybrid_property
    def vie_max(self):
        if self.pdv is not None:
            return self.pdv
        if self.blessure is None or self.blessure == 0:
            return self.base_pdv_max
        elif self.base_pdv_max is not None:
            return math.ceil(self.base_pdv_max * (100 - max(1, self.blessure - 4)) / 100)
        return None

    @hybrid_property
    def nom_complet(self):
        if self.troll is not None:
            return self.troll.nom_complet
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
                        troll_private = TrollPrivate(troll_id=self.troll_id, viewer_id=partage.user_id,
                                                     last_reconciliation_at=now, last_reconciliation_by=self.viewer_id)
                        sg.copy_properties(self, troll_private, ['pos_x', 'pos_y', 'pos_n'], False)
                        sg.db.upsert(troll_private, propagate=False)
                # Sharing Event or Profile
                if (my_partage.sharingEvents and self.viewer_id != user.id) or (my_partage.sharingProfile and self.viewer_id == user.id):
                    for partage in my_partage.coterie.partages_actifs:
                        troll_private = TrollPrivate(troll_id=self.troll_id, viewer_id=partage.user_id,
                                                     last_reconciliation_at=now,
                                                     last_reconciliation_by=self.viewer_id)
                        sg.copy_properties(self, troll_private,
                                           ['pos_x', 'pos_y', 'pos_n', 'blessure', 'pdv', 'malus_arm', 'fatigue',
                                            'camouflage', 'invisible', 'immobile', 'terre', 'course', 'levite',
                                            'nb_att_sub', 'nb_parade_prog', 'nb_ctr_att_prog', 'nb_retraite_prog',
                                            'dir_retraite_prog', 'base_concentration', 'bonus_concentration_phy',
                                            'bonus_concentration_mag', 'last_sp4_update_at',
                                            'last_seen_at', 'last_event_at'], False)
                        if my_partage.sharingProfile:
                            sg.copy_properties(self, troll_private,
                                               ['pi', 'pi_disp', 'pa', 'next_dla', 'malus_poids_phy', 'malus_poids_mag'],
                                               False)
                        for attr in ['pdv', 'att', 'esq', 'deg', 'reg', 'arm', 'vue', 'tour']:
                            attr_min = 'base_' + attr + '_min'
                            attr_max = 'base_' + attr + '_max'
                            setattr(troll_private, attr_min, sg.do_unless_none(max, (getattr(troll_private, attr_min), getattr(self, attr_min))))
                            setattr(troll_private, attr_max, sg.do_unless_none(min, (getattr(troll_private, attr_max), getattr(self, attr_max))))
                            if my_partage.sharingProfile:
                                sg.copy_properties(self, troll_private, ['bonus_' + attr + '_phy', 'bonus_' + attr + '_mag'], False)
                        sg.db.upsert(troll_private, propagate=False)
