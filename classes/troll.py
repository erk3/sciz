#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import re, datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
import modules.globals as sg

# Class of a troll
class TROLL(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'trolls'
    __table_args__ = (PrimaryKeyConstraint('id', 'group_id'), )
    # Numéro de Troll
    id = Column(Integer)
    # ID du groupe d'appartenance
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    # ID de l'utilisateur de rattachement
    user_id = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"))
    # Condition if notifications have to be pushed for this troll
    shadowed = Column(Boolean, default=False)
    # Horodatage du dernier appel aux SP
    last_mhsp4_call = Column(DateTime)
    # Nom
    nom = Column(String(50))
    # Race
    race = Column(String(10))
    # Niveau
    niv = Column(Integer)
    # Nombre de kills
    nb_kill = Column(Integer)
    # Nombre de morts
    nb_mort = Column(Integer)
    # Nombre de mouches
    nb_mouche = Column(Integer)
    # Numéro de guilde
    id_guilde = Column(Integer)
    # Numéro de rang dans la guilde
    rang_guilde = Column(Integer)
    # Etat
    etat = Column(String(50))
    # Est un PNJ ?
    pnj = Column(Boolean)
    # Est un ami MH ?
    ami_mh = Column(Boolean)
    # Date d'inscription
    inscription = Column(DateTime)
    # URL du blason (profil public)
    blason_url = Column(String(500))
    # Position axe X
    pos_x = Column(Integer)
    # Position axe Y
    pos_y = Column(Integer)
    # Posistion axe N
    pos_n = Column(Integer)
    # Date de dernière vue à la position
    last_seen = Column(DateTime)
    # Nombre de points de vie restants
    pv = Column(Integer)
    # Bonus de PdV physique
    bonus_pv_phy = Column(Integer)
    # Bonus de PdV magique
    bonus_pv_mag = Column(Integer)
    # Nombre maximum de points de vie (hors bonus)
    base_pv_max = Column(Integer)
    # Bonus de PdV max physique
    bonus_pv_max_phy = Column(Integer)
    # Bonus de PdV max magique
    bonus_pv_max_mag = Column(Integer)
    # Nombre maximum de points de vie avec bonus
    base_bonus_pv_max = Column(Integer)
    # Nombre de points d'actions restants
    pa = Column(Integer)
    # Horodatage de la prochaine DLA
    dla = Column(DateTime)
    # Nombre de D6 d'attaque
    base_att = Column(Integer)
    # Bonus d'attaque physique
    bonus_att_phy = Column(Integer)
    # Bonus d'attaque magique
    bonus_att_mag = Column(Integer)
    # Nombre de D6 d'esquive
    base_esq = Column(Integer)
    # Bonus d'esquive physique
    bonus_esq_phy = Column(Integer)
    # Bonus d'esquive magique
    bonus_esq_mag = Column(Integer)
    # Nombre de D3 de dégâts
    base_deg = Column(Integer)
    # Bonus de dégâts physique
    bonus_deg_phy = Column(Integer)
    # Bonus de dégâts magique
    bonus_deg_mag = Column(Integer)
    # Nombre de D3 de régénération
    base_reg = Column(Integer)
    # Bonus de régénération physique
    bonus_reg_phy = Column(Integer)
    # Bonus de régénération magique
    bonus_reg_mag = Column(Integer)
    # Nombre de cases de vue
    base_vue = Column(Integer)
    # Bonus de vue physique
    bonus_vue_phy = Column(Integer)
    # Bonus de vue magique
    bonus_vue_mag = Column(Integer)
    # Nombre de D3 d'armure physique naturelle
    base_arm_phy = Column(Integer)
    # Nombre de dés d'armure en moins à ce stade du tour
    malus_base_arm_phy = Column(Integer)
    # Bonus d'armure physique apporté par l'équipement
    bonus_arm_phy = Column(Integer)
    # Bonus d'armure magique
    bonus_arm_mag = Column(Integer)
    # Nombre de points de Maitrise Magique de base
    base_mm = Column(Integer)
    # Bonus de MM physique
    bonus_mm_phy = Column(Integer)
    # Bonus de MM magique
    bonus_mm_mag = Column(Integer)
    # Nombre de points de Résistance Magique de base
    base_rm = Column(Integer)
    # Bonus de RM physique
    bonus_rm_phy = Column(Integer)
    # Bonus de RM magique
    bonus_rm_mag = Column(Integer)
    # Nombre d'attaques subies dans le tour
    nb_att_sub = Column(Integer)
    # Nombre de points de fatigue actuels
    fatigue = Column(Integer)
    # Est intangible ?
    intangible = Column(Boolean)
    # Est camouflé ?
    camouflage = Column(Boolean)
    # Est invisible ?
    invisible = Column(Boolean)
    # Est immobilisé ?
    immobile = Column(Boolean)
    # Est à terre ?
    terre = Column(Boolean)
    # Est en course ?
    course = Column(Boolean)
    # Est en lévitation ?
    levite = Column(Boolean)
    # Nombre de parades programmées
    nb_parade_prog = Column(Integer)
    # Nombre de contre-attaques programmées
    nb_ctr_att_prog = Column(Integer)
    # Durée de base du tour en minutes
    base_tour = Column(Integer)
    # Bonus de durée du tour physique
    bonus_tour_phy = Column(Integer)
    # Bonus de durée du tour magique
    bonus_tour_mag = Column(Integer)
    # Poids de base en minutes
    base_poids = Column(Integer)
    # Malus de poids physique
    malus_poids_phy = Column(Integer)
    # Malus de poids magique
    malus_poids_mag = Column(Integer)
    # Concentration de base en %
    base_concentration = Column(Integer)
    # Bonus de concentration physique en %
    bonus_concentration_phy = Column(Integer)
    # Bonus de concentration magique en %
    bonus_concentration_mag = Column(Integer)
    # Nombre de PI totaux
    pi = Column(Integer)
    # Nombre de retraite programmées
    nb_retraite_prog = Column(Integer)
    # Direction des retraites par ordre chronologique
    dir_retraite = Column(String(50))

    # AA stats
    aa_pv_min = Column(Integer)
    aa_pv_max = Column(Integer)
    aa_base_att_min = Column(Integer)
    aa_base_att_max = Column(Integer)
    aa_base_esq_min = Column(Integer)
    aa_base_esq_max = Column(Integer)
    aa_base_deg_min = Column(Integer)
    aa_base_deg_max = Column(Integer)
    aa_base_reg_min = Column(Integer)
    aa_base_reg_max = Column(Integer)
    aa_base_arm_phy_min = Column(Integer)
    aa_base_arm_phy_max = Column(Integer)
    aa_base_vue_min = Column(Integer)
    aa_base_vue_max = Column(Integer)
    
    @hybrid_property
    def pseudo(self):
        if self.user and self.user.pseudo:
            return self.user.pseudo
        return self.nom

    # Associations Many-To-Many
    capas = relationship("AssocTrollsCapas", back_populates="troll")
    # Associations One-To-Many
    user = relationship('USER', back_populates='trolls')
    group = relationship('GROUP', back_populates='trolls')
    # Associations Many-To-One
    idts = relationship('IDT', primaryjoin="and_(TROLL.id==IDT.troll_id, TROLL.group_id==IDT.group_id)", back_populates='troll')
    idcs = relationship('IDC', primaryjoin="and_(TROLL.id==IDC.troll_id, TROLL.group_id==IDC.group_id)", back_populates='troll')
    pieges = relationship('PIEGE', primaryjoin="and_(TROLL.id==PIEGE.troll_id, TROLL.group_id==PIEGE.group_id)", back_populates='troll')
    portals = relationship('PORTAL', primaryjoin="and_(TROLL.id==PORTAL.troll_id, TROLL.group_id==PORTAL.group_id)", back_populates='troll')
    cdms = relationship('CDM', primaryjoin="and_(TROLL.id==CDM.troll_id, TROLL.group_id==CDM.group_id)", back_populates='troll')
    aas = relationship('AA', primaryjoin="and_(TROLL.id==AA.troll_id, TROLL.group_id==AA.group_id)", back_populates='troll')
    atts = relationship('BATTLE', primaryjoin="and_(BATTLE.att_troll_id==TROLL.id, BATTLE.group_id==TROLL.group_id)", back_populates='att_troll')
    defs = relationship('BATTLE', primaryjoin="and_(BATTLE.def_troll_id==TROLL.id, BATTLE.group_id==TROLL.group_id)", back_populates='def_troll')
    
    # Constructor is handled by SqlAlchemy, do not override

    # Populate object from a AA
    def populate_from_aa(self, aa):
        self.id = aa.troll_cible_id
        self.group_id = aa.group_id
        self.nom = aa.troll_cible_name
        self.niv = aa.niv

        self.aa_pv_min = sg.do_unless_none((max), (self.aa_pv_min, aa.pv_min))
        self.aa_base_att_min = sg.do_unless_none((max), (self.aa_base_att_min, aa.att_min))
        self.aa_base_esq_min = sg.do_unless_none((max), (self.aa_base_esq_min, aa.esq_min))
        self.aa_base_deg_min = sg.do_unless_none((max), (self.aa_base_deg_min, aa.deg_min))
        self.aa_base_reg_min = sg.do_unless_none((max), (self.aa_base_reg_min, aa.reg_min))
        self.aa_base_arm_phy_min = sg.do_unless_none((max), (self.aa_base_arm_phy_min, aa.arm_phy_min))
        self.aa_base_vue_min = sg.do_unless_none((max), (self.aa_base_vue_min, aa.vue_min))
        
        self.aa_pv_max = sg.do_unless_none((min), (self.aa_pv_max, aa.pv_max))
        self.aa_base_att_max = sg.do_unless_none((min), (self.aa_base_att_max, aa.att_max))
        self.aa_base_esq_max = sg.do_unless_none((min), (self.aa_base_esq_max, aa.esq_max))
        self.aa_base_deg_max = sg.do_unless_none((min), (self.aa_base_deg_max, aa.deg_max))
        self.aa_base_reg_max = sg.do_unless_none((min), (self.aa_base_reg_max, aa.reg_max))
        self.aa_base_arm_phy_max = sg.do_unless_none((min), (self.aa_base_arm_phy_max, aa.arm_phy_max))
        self.aa_base_vue_max = sg.do_unless_none((min), (self.aa_base_vue_max, aa.vue_max))
        
    def estimate_next_dla(self):
        try:
            self.nextDLA = None
            # Add base tour
            mins = self.base_tour
            # Add stuff weight
            mins += self.base_poids + self.malus_poids_phy + self.malus_poids_mag
            # Add wound malus
            mins += (250 * (self.base_bonus_pv_max - self.pv)) // self.base_bonus_pv_max
            # Add bonuses (templates, flies, etc.)
            # (phy => mouches / natif equip (grimoire,etc.) ; mag => templates) et autres (pouvoirs, events) ?
            mins += self.bonus_tour_phy + self.bonus_tour_mag # + self.bonus_tour (?.)
            # Keep the result at minimum base tour
            mins = max(self.base_tour, mins)
            # Do the actual estimation
            self.nextDLA = self.dla + datetime.timedelta(minutes = mins)
            return self.nextDLA
        except TypeError as e:
            # Missing data (probably no previous success call to MH SP)
            return None
    
    def stringify_name(self, str_format=None):
        if str_format:
            return str_format.format(o=self)
        self.s_nom_troll = ('%s (%d)' % (self.nom, self.id))
        if self.user and self.user.pseudo:
            self.s_nom_troll = ('%s (%d)' % (self.user.pseudo, self.id))
        return self.s_nom_troll

    def stringify(self, reprs, short, attrs):
        # Build the string representations provided
        for (key, value) in reprs:
            s = ''
            try:
                if key.startswith('s_'):
                    setattr(self, key, value)
                    continue
                elif hasattr(self, key) and getattr(self, key) is not None:
                    if isinstance(getattr(self, key), bool):
                        # s = value.format(sg.boolean2French(getattr(self, key), value))
                        s = sg.boolean2French(getattr(self, key), value)
                    else:
                        s = value.format(getattr(self, key))
                elif hasattr(self, key + '_min') or hasattr(self, key + '_max'):
                    s = sg.str_min_max(getattr(self, key+ '_min'), getattr(self, key + '_max'))
                    if s is not None:
                        s = value.format(s)
                    elif hasattr(self, 'aa_' + key + '_min') or hasattr(self, 'aa_' + key + '_max'):
                        s = sg.str_min_max(getattr(self, 'aa_' + key + '_min'), getattr(self, 'aa_' + key + '_max'))
                        s = value.format(s) if s is not None else ''
                    else:
                        s = ''
            except KeyError as e:
                pass
            setattr(self, 's_' + key, s)
        # Compute some things
        self.s_troll_nom = self.stringify_name()
        self.s_last_mhsp4_call = sg.format_time(self.last_mhsp4_call, self.s_time) if self.last_mhsp4_call else ''
        self.s_last_update = self.s_last_update.format(o=self) if self.s_last_mhsp4_call != '' else ''
        self.s_last_seen = sg.format_time(self.last_seen, self.s_time) if self.last_seen else ''
        self.s_last_seen_at = self.s_last_seen_at.format(o=self) if self.last_seen else ''
        self.s_dla = sg.format_time(self.dla, self.s_time) if self.dla else ''
        self.s_next_dla = sg.format_time(self.estimate_next_dla(), self.s_time)
        self.s_dla_full = self.s_dla_full.format(o=self) if self.s_dla != '' else ''
        self.s_pos = self.s_pos.format(o=self) if self.s_pos_x != '' else ''
        self.s_pv_ratio = self.s_pv_ratio.format(o=self) if self.s_pv != '' else ''
        self.s_att = self.s_att.format(o=self) if self.s_base_att != '' else ''
        self.s_esq = self.s_esq.format(o=self) if self.s_base_esq != '' else ''
        self.s_deg = self.s_deg.format(o=self) if self.s_base_deg != '' else ''
        self.s_reg = self.s_reg.format(o=self) if self.s_base_reg != '' else ''
        self.s_arm = self.s_arm.format(o=self) if self.s_base_arm_phy != '' else ''
        self.s_vue = self.s_vue.format(o=self) if self.s_base_vue != '' else ''
        self.s_mm = self.s_mm.format(o=self) if self.s_base_mm != '' else ''
        self.s_rm = self.s_rm.format(o=self) if self.s_base_rm != '' else ''
        self.s_comps = self.s_sep.join([sg.pretty_print(comp, False).decode(sg.DEFAULT_CHARSET) for comp in self.capas if comp.type == u"Compétence"])
        self.s_sorts = self.s_sep.join([sg.pretty_print(sort, False).decode(sg.DEFAULT_CHARSET) for sort in self.capas if sort.type == u"Sortilège"])
        # Filter out attrs not wanted (but separator)
        if attrs is not None:
            for match in re.findall('\{o\.s_(.+?)\}', self.s_troll_stats):
                if match not in attrs and match != "sep":
                    self.s_troll_stats = re.sub(r'\{o\.s_%s\}' % (match), '', self.s_troll_stats)
        # Return the final formated representation
        self.s_etat = self.s_etat.format(o=self)
        self.s_troll_stats = self.s_troll_stats.format(o=self)
        res = self.s_long
        res = res.format(o=self)
        res = res.encode(sg.DEFAULT_CHARSET).decode('string-escape').decode(sg.DEFAULT_CHARSET)
        # Adjust some things about spacing, None values and line break
        res = re.sub(r'None', '', res)
        res = re.sub(r'%s{2,}' % self.s_delimiter, '%s' % (self.s_delimiter), res)
        res = re.sub(r'%s\s*%s' % (self.s_delimiter, self.s_sep, ), '%s' % self.s_sep, res)
        res = re.sub(r'%s\s*%s' % (self.s_sep, self.s_delimiter, ), '%s' % self.s_sep, res)
        res = re.sub(r'\s*%s+\s*' % self.s_sep, '%s' % (self.s_sep), res)
        res = re.sub(r'%s$' % self.s_sep, '', res)
        if attrs is not None and len(attrs) == 1 and len(re.findall(self.s_sep, res)) <= 1:
            res = re.sub(r'%s' % self.s_sep, ' ', res)
        res = re.sub(r' +', ' ', res)
        return res

    def __getattr__(self, name):
        if hasattr(self, name) or name.startswith('_'):
            return super(TROLL, self).__getattribute__(name)
        else:
            return None # Trick for the stringify logic (avoiding the raise of an error)
