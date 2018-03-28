#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import re
import modules.globals as sg

# Class of a Mob
class MOB(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'mobs'
    __table_args__ = (PrimaryKeyConstraint('id', 'group_id'), )
    # ID unique du monstre
    id = Column(Integer)
    # SCIZ notifs ?
    sciz_notif = Column(Boolean)
    # ID du groupe
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    # ID du metamob
    metamob_id = Column(Integer, ForeignKey('metamobs.id'))
    # Nom (incluant modificateurs)
    nom = Column(String(50))
    # Type (Race) du monstre
    type = Column(String(50))
    # Tatouage
    tag = Column(String(50))
    # Age
    age = Column(String(50))
    # Pourcentage de blessure
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

    # Associations Many-To-One
    cdms = relationship("CDM", primaryjoin="and_(MOB.id==CDM.mob_id, MOB.group_id==CDM.group_id)", back_populates="mob")
    atts = relationship("BATTLE", primaryjoin='and_(MOB.id==BATTLE.att_mob_id, MOB.group_id==BATTLE.group_id)', back_populates="att_mob")
    defs = relationship("BATTLE", primaryjoin='and_(MOB.id==BATTLE.def_mob_id, MOB.group_id==BATTLE.group_id)', back_populates="def_mob")
    # Assosiations One-To-Many
    metamob = relationship("METAMOB", back_populates="mobs")
    group = relationship("GROUP", back_populates="mobs")

    # Constructor is handled by SqlAlchemy do not override
    
    # Loop over every metamobs in the list to find the longest one matching the mob name...
    def link_metamob(self, metamobs):
        result_id = -1
        result_nom = ''
        if self.nom != None:
            for metamob in metamobs:
                if metamob.nom in self.nom and len(metamob.nom) > len(result_nom):
                    result_nom = metamob.nom
                    result_id = metamob.id
            if result_id > 0:
                self.metamob_id = result_id
            else:
                sg.logger.warning('Cannot match \'%s\' to a metamob' % self.nom)
        else:
            sg.logger.error('Mob has no name, cannot search for a metamob to link')

    # Populate object from a CDM
    def populate_from_cdm(self, obj):
        self.id = obj.mob_id
        self.group_id = obj.group_id
        self.nom = obj.mob_name
        self.tag = obj.mob_tag
        self.age = obj.mob_age
        sg.copy_properties(obj, self, ['type', 'blessure', 'niv_min', 'niv_max', 'pv_min', 'pv_max', 'att_min', 'att_max', 'esq_min', 'esq_max', 'deg_min', 'deg_max', 'reg_min', 'reg_max', 'arm_phy_min', 'arm_phy_max', 'vue_min', 'vue_max', 'capa_desc', 'capa_effet', 'capa_tour', 'mm_min', 'mm_max', 'rm_min', 'rm_max', 'nb_att_tour', 'vit_dep', 'vlc', 'att_dist', 'dla', 'tour_min', 'tour_max', 'chargement', 'bonus_malus', 'portee_capa'], True)

    # Update mob definition with the more accurate value
    def update_from_new(self, mob):
        sg.copy_properties(mob, self, ['age', 'blessure', 'capa_desc', 'capa_effet', 'capa_tour', 'nb_att_tour', 'vit_dep', 'vlc', 'att_dist', 'dla', 'chargement', 'bonus_malus', 'portee_capa'], False)
        
        self.niv_min = sg.do_unless_none((max), (self.niv_min, mob.niv_min))
        self.pv_min = sg.do_unless_none((max), (self.pv_min, mob.pv_min))
        self.att_min = sg.do_unless_none((max), (self.att_min, mob.att_min))
        self.esq_min = sg.do_unless_none((max), (self.esq_min, mob.esq_min))
        self.deg_min = sg.do_unless_none((max), (self.deg_min, mob.deg_min))
        self.reg_min = sg.do_unless_none((max), (self.reg_min, mob.reg_min))
        self.arm_phy_min = sg.do_unless_none((max), (self.arm_phy_min, mob.arm_phy_min))
        self.vue_min = sg.do_unless_none((max), (self.vue_min, mob.vue_min))
        self.mm_min = sg.do_unless_none((max), (self.mm_min, mob.mm_min))
        self.rm_min = sg.do_unless_none((max), (self.rm_min, mob.rm_min))
        self.tour_min = sg.do_unless_none((max), (self.tour_min, mob.tour_min))
        
        self.niv_max = sg.do_unless_none((min), (self.niv_max, mob.niv_max))
        self.pv_max = sg.do_unless_none((min), (self.pv_max, mob.pv_max))
        self.att_max = sg.do_unless_none((min), (self.att_max, mob.att_max))
        self.esq_max = sg.do_unless_none((min), (self.esq_max, mob.esq_max))
        self.deg_max = sg.do_unless_none((min), (self.deg_max, mob.deg_max))
        self.reg_max = sg.do_unless_none((min), (self.reg_max, mob.reg_max))
        self.arm_phy_max = sg.do_unless_none((min), (self.arm_phy_max, mob.arm_phy_max))
        self.vue_max = sg.do_unless_none((min), (self.vue_max, mob.vue_max))
        self.mm_max = sg.do_unless_none((min), (self.mm_max, mob.mm_max))
        self.rm_max = sg.do_unless_none((min), (self.rm_max, mob.rm_max))
        self.tour_max = sg.do_unless_none((min), (self.tour_max, mob.tour_max))

    def stringify_name(self, str_format=None):
        if str_format:
            return str_format.format(o=self)
        if self.tag:
            return '%s [%s] %s (%d)' % (self.nom, self.age, self.tag, self.id)
        else:
            return '%s [%s] (%d)' % (self.nom, self.age, self.id)
    
    def stringify(self, reprs, short, attrs):
        self.s_mob_nom = self.stringify_name()
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
                    s = sg.str_min_max(getattr(self, key + '_min'), getattr(self, key + '_max'))
                    s = value.format(s) if s is not None else ''
            except KeyError as e:
                pass
            setattr(self, 's_' + key, s)
        # Add the capa
        self.s_capa = self.s_capa_effet
        if self.s_capa_tour:
            self.s_capa = '%s %s %s' % (self.s_capa, self.s_delimiter, self.s_capa_tour)
        if self.s_capa_desc:
            self.s_capa = '%s %s %s' % (self.s_capa_desc, self.s_delimiter, self.s_capa)
        # Filter out attrs not wanted (but separator)
        if attrs is not None:
            for match in re.findall('\{o\.s_(.+?)\}', self.s_mob_stats):
                if match not in attrs and match != "sep":
                    self.s_mob_stats = re.sub(r'\{o\.s_%s\}' % (match), '', self.s_mob_stats)
        # Return the final formated representation
        self.s_mob_stats = self.s_mob_stats.format(o=self)
        res = self.s_long
        res = res.format(o=self)
        res = res.encode(sg.DEFAULT_CHARSET).decode('string-escape').decode(sg.DEFAULT_CHARSET)
        # Adjust some things about spacing, None values and line break
        res = re.sub(r'None', '', res)
        res = re.sub(r'\s*%s+\s*' % self.s_sep, '%s' % (self.s_sep), res)
        res = re.sub(r'%s$' % self.s_sep, '', res)
        if attrs is not None and len(attrs) == 1:
            res = re.sub(r'%s' % self.s_sep, ' ', res)
        res = re.sub(r' +', ' ', res)
        return res

    def __getattr__(self, name):
        if hasattr(self, name) or name.startswith('_'):
            return super(MOB, self).__getattribute__(name)
        else:
            return None # Trick for the stringify logic (avoiding the raise of an error)
