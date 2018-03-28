#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import re, datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a CDM
class CDM(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'cdms'
    __table_args__ = (PrimaryKeyConstraint('id', 'group_id'), )
    # ID unique
    id = Column(Integer, autoincrement=True)
    # Horodatage de la CDM
    time = Column(DateTime)
    # ID du troll 
    troll_id = Column(Integer, ForeignKey('trolls.id'))
    # ID du monstre
    mob_id = Column(Integer, ForeignKey('mobs.id'))
    # ID du groupe
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    # Niveau de compétence de la CDM
    comp_niv = Column(Integer)
    # Pourcentage de blessure du monstre
    blessure = Column(Integer)
    # Niveau minimum
    niv_min = Column(Integer)
    # Niveau maximum
    niv_max = Column(Integer)
    # Points de Vie minimum
    pv_min = Column(Integer)
    # Points de Vie maximum
    pv_max = Column(Integer)
    # Attaque minimum en D6
    att_min = Column(Integer)
    # Attaque maximum en D6
    att_max = Column(Integer)
    # Esquive minimum en D6
    esq_min = Column(Integer)
    # Esquive maximum en D6
    esq_max = Column(Integer)
    # Dégâts minimum en D3
    deg_min = Column(Integer)
    # Dégâts maximum en D3
    deg_max = Column(Integer)
    # Régénération minimum en D3
    reg_min = Column(Integer)
    # Régénération maximum en D3
    reg_max = Column(Integer)
    # Armure physique minimum
    arm_phy_min = Column(Integer)
    # Armure physique maximum
    arm_phy_max = Column(Integer)
    # Vue minimum en nombre de cases
    vue_min = Column(Integer)
    # Vue maximum en nombre de cases
    vue_max = Column(Integer)
    # Descritpion de la capacité spéciale
    capa_desc = Column(String(150))
    # Effet de la capacité spéciale
    capa_effet = Column(String(150))
    # Nombre de tours d'effet de la capacité spéciale
    capa_tour = Column(Integer)
    # Maitrise Magique minimum
    mm_min = Column(Integer)
    # Maitrise Magique maximum
    mm_max = Column(Integer)
    # Résistance Magique minimum
    rm_min = Column(Integer)
    # Résistance Magique maximum
    rm_max = Column(Integer)
    # Nombre d'attaque par tour
    nb_att_tour = Column(Integer)
    # Vitesse de déplacement
    vit_dep = Column(String(10))
    # Voir la caché ?
    vlc = Column(Boolean)
    # Attaque à distance ?
    att_dist = Column(Boolean)
    # Moment de la DLA
    dla = Column(String(50))
    # Tour minimum en heure
    tour_min = Column(Integer)
    # Tour maximum en heure
    tour_max = Column(Integer)
    # Chargement de trésors
    chargement = Column(String(50))
    # Bonus et Malus en cours 
    bonus_malus = Column(String(150))
    # Portée du pouvoir (capacité spéciale)
    portee_capa = Column(String(50))

    # Associations One-To-Many
    troll = relationship("TROLL", primaryjoin="and_(CDM.troll_id==TROLL.id, CDM.group_id==TROLL.group_id)", back_populates="cdms")
    mob = relationship("MOB", primaryjoin="and_(CDM.mob_id==MOB.id, CDM.group_id==MOB.group_id)", back_populates="cdms")
    group = relationship("GROUP", back_populates="cdms")
    # Association One-To-One
    event = relationship("EVENT", primaryjoin="and_(CDM.id==EVENT.cdm_id, CDM.group_id==EVENT.group_id)", back_populates="cdm", uselist=False)

    # Constructor is handled by SqlAlchemy do not override
    
    # Additional build logics
    def build(self):
        self.time = datetime.datetime.strptime(self.time, '%d/%m/%Y  %H:%M:%S')
        # CDM Niv 1
        self.niv_min = self.niv_min or self.niv_sup or self.niv_eq
        self.niv_max = self.niv_max or self.niv_inf or self.niv_eq
        self.pv_min = self.pv_min or self.pv_sup or self.pv_eq
        self.pv_max = self.pv_max or self.pv_inf or self.pv_eq
        self.att_min = self.att_min or self.att_sup or self.att_eq
        self.att_max = self.att_max or self.att_inf or self.att_eq
        self.esq_min = self.esq_min or self.esq_sup or self.esq_eq
        self.esq_max = self.esq_max or self.esq_inf or self.esq_eq
        self.deg_min = self.deg_min or self.deg_sup or self.deg_eq
        self.deg_max = self.deg_max or self.deg_inf or self.deg_eq
        self.reg_min = self.reg_min or self.reg_sup or self.reg_eq
        self.reg_max = self.reg_max or self.reg_inf or self.reg_eq
        self.arm_phy_min = self.arm_phy_min or self.arm_phy_sup or self.arm_phy_eq
        self.arm_phy_max = self.arm_phy_max or self.arm_phy_inf or self.arm_phy_eq
        self.vue_min = self.vue_min or self.vue_sup or self.vue_eq
        self.vue_max = self.vue_max or self.vue_inf or self.vue_eq
        # CDM Niv 2
        if hasattr(self, 'mm_eq'):
            self.mm_min = self.mm_min or self.mm_sup or self.mm_eq
            self.mm_max = self.mm_max or self.mm_inf or self.mm_eq
        if hasattr(self, 'rm_eq'):
            self.rm_min = self.rm_min or self.rm_sup or self.rm_eq
            self.rm_max = self.rm_max or self.rm_inf or self.rm_eq
        if self.capa_effet is not None:
            self.capa_effet = re.sub(r'(\n|\|$)', ' ', self.capa_effet)
        self.vlc = sg.parseFrenchBoolean(self.vlc)
        self.att_dist = sg.parseFrenchBoolean(self.att_dist)
        # CDM Niv 3 & 4
        if hasattr(self, 'tour_eq'):
            self.tour_min = self.tour_min or self.tour_sup or self.tour_eq
            self.tour_max = self.tour_max or self.tour_inf or self.tour_eq
                    
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
                        s = value.format(sg.boolean2French(getattr(self, key)))
                    else:
                        s = value.format(getattr(self, key))
                elif hasattr(self, key + '_min') or hasattr(self, key + '_max'):
                    s = sg.str_min_max(getattr(self, key+ '_min'), getattr(self, key + '_max'))
                    s = value.format(s) if s is not None else ''
            except KeyError as e:
                pass
            setattr(self, 's_' + key, s)
        # Add the time
        self.s_time = sg.format_time(self.time, self.s_time)
        # Add the att an def troll/mob names
        self.s_troll_nom = self.troll.stringify_name()
        self.s_mob_nom = self.mob.stringify_name()
        # Add the capa
        self.s_capa = self.s_capa_effet
        if self.s_capa_tour:
            self.s_capa = '%s %s %s' % (self.s_capa, self.s_delimiter, self.s_capa_tour)
        if self.s_capa_desc:
            self.s_capa = '%s %s %s' % (self.s_capa_desc, self.s_delimiter, self.s_capa)
        # Return the final formated representation
        if short:
            res = self.s_short
        else:
            res = self.s_long
        self.s_cdm_stats = self.s_cdm_stats.format(o=self)
        res = res.format(o=self)
        res = res.encode(sg.DEFAULT_CHARSET).decode('string-escape').decode(sg.DEFAULT_CHARSET)
        res = re.sub(r'None', '', res)
        res = re.sub(r'\s*%s+\s*' % self.s_sep, '%s' % (self.s_sep), res)
        res = re.sub(r'%s$' % self.s_sep, '', res)
        res = re.sub(r' +', ' ', res)
        return res

    def __getattr__(self, name):
        if hasattr(self, name) or name.startswith('_'):
            return super(CDM, self).__getattribute__(name)
        else:
            return None # Trick for the stringify logic (avoiding the raise of an error)
