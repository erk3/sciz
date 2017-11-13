#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import re, datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a troll
class TROLL(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'trolls'
    __table_args__ = (PrimaryKeyConstraint('id', 'group_id'), )
    # Numéro de Troll
    id = Column(Integer)
    # ID du groupe d'appartenance
    group_id = Column(Integer, ForeignKey('groups.id'))
    # ID de l'utilisateur de rattachement
    user_id = Column(Integer, ForeignKey('users.id'))
    # Condition if notifications have to be pushed for this troll
    sciz_notif = Column(Boolean)
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
    blason_url = Column(String(150))
    # Position axe X
    pos_x = Column(Integer)
    # Position axe Y
    pos_y = Column(Integer)
    # Posistion axe N
    pos_n = Column(Integer)
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
    # Bonus de durée du tour (???)
    bonus_tour = Column(Integer)
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
    # Limite effective de la vue
    limite_vue = Column(Integer)
    # Nombre de retraite programmées
    nb_retraite_prog = Column(Integer)
    # Direction des retraites par ordre chronologique
    dir_retraite = Column(String(10))

    # Associations One-To-Many
    user = relationship('USER', back_populates='trolls')
    group = relationship('GROUP', back_populates='trolls')
    # Associations Many-To-One
    pieges = relationship('PIEGE', primaryjoin="and_(TROLL.id==PIEGE.troll_id, TROLL.group_id==PIEGE.group_id)", back_populates='troll')
    cdms = relationship('CDM', primaryjoin="and_(TROLL.id==CDM.troll_id, TROLL.group_id==CDM.group_id)", back_populates='troll')
    atts = relationship('BATTLE', primaryjoin="and_(BATTLE.att_troll_id==TROLL.id, BATTLE.group_id==TROLL.group_id)", back_populates='att_troll')
    defs = relationship('BATTLE', primaryjoin="and_(BATTLE.def_troll_id==TROLL.id, BATTLE.group_id==TROLL.group_id)", back_populates='def_troll')
    
    # Constructor is handled by SqlAlchemy, do not override

    def update_from_new(self, troll, event = None):
        # Update new troll with event
        if event != None:
            troll.pv = event.vie if event.vie != None else troll.pv
            # Heal
            troll.pv = max(self.base_bonus_pv_max, self.pv + int(event.soin)) if event.soin != None and self.base_bonus_pv_max != None else troll.pv
            # Blessure
            troll.pv = max(0, self.pv - int(event.blessure)) if event.blessure != None and self.pv != None else troll.pv
        # Actual copy
        lst = ['pv']
        if self.nom == None: # Update the name of the troll only if not known so far (on the fly troll adding case)
            lst.append('nom')
        sg.copy_properties(troll, self, lst, False)

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
    
    # Generate the string representation of each attribute and return the list of attributes printable
    def stringify(self):
        # Generate STR representation
        # TODO: only use s_ attr for pprinter (based on confs/sciz.ini)? Then this will be useful
        #plain_attrs = ['pv','niv']
        #for attr in plain_attrs:
        #    val = getattr(self, attr)
        #    setattr(self, 's_' + attr, val)
        self.s_nom_full = self.nom + ' (' +  str(self.id) + ')' if self.nom else str(self.id)
        self.s_nom_short = '~' + self.user.pseudo if self.user and self.user.pseudo else self.s_nom_full
        self.s_dla = sg.format_time(self.dla) if self.dla else None
        self.next_dla = self.estimate_next_dla()
        self.s_next_dla = sg.format_time(self.next_dla) if self.next_dla else None
