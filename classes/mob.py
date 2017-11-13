#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
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
    group_id = Column(Integer, ForeignKey('groups.id'))
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
                print 'Cannot match name of mob to a metamob'
        else:
            print 'Mob has no name, cannot search for a metamob to link'

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

    # Generate the string representation of each attribute and return the list of attributes printable
    def stringify(self):
        # Generate STR representation
        self.s_tag = ' ' + self.tag if self.tag else ''
        self.s_nom_short = self.nom + ' (' + str(self.id) + ')'
        self.s_nom_full = self.nom + ' [' + self.age + ']' + self.s_tag + ' (' + str(self.id) + ')'
        self.s_blessure = self.blessure if self.blessure != None else '?'
        self.s_niv = sg.str_min_max(self.niv_min, self.niv_max)
        self.s_pv = sg.str_min_max(self.pv_min, self.pv_max)
        self.s_att = sg.str_min_max(self.att_min, self.att_max)
        self.s_esq = sg.str_min_max(self.esq_min, self.esq_max)
        self.s_deg = sg.str_min_max(self.deg_min, self.deg_max)
        self.s_reg = sg.str_min_max(self.reg_min, self.reg_max)
        self.s_vue = sg.str_min_max(self.vue_min, self.vue_max)
        self.s_arm_phy = sg.str_min_max(self.arm_phy_min, self.arm_phy_max)
        self.s_mm = sg.str_min_max(self.mm_min, self.mm_max)
        self.s_rm = sg.str_min_max(self.rm_min, self.rm_max)
        self.s_tour = sg.str_min_max(self.tour_min, self.tour_max)
        if self.capa_desc:
            self.s_capa = self.capa_desc + ' (Affecte : ' + self.capa_effet + ')'
        if self.capa_tour:
            self.s_capa += ' ' + str(self.capa_tour) + 'T'
        if self.portee_capa:
            self.s_capa += ' (' + self.portee_capa + ')' 
        self.s_vlc = 'Oui' if self.vlc else 'Non'
        self.s_att_dist = 'Oui' if self.att_dist else 'Non'
        self.s_vit = self.vit_dep
        self.s_nb_att_tour = self.nb_att_tour
        self.s_dla = self.dla
        self.s_chargement = self.chargement
        self.s_bonus_malus = self.bonus_malus
