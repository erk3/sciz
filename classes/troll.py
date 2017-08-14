#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import re, datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a troll
class TROLL(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'trolls'
    id = Column(Integer, primary_key=True)      # Numéro de Troll
    sciz_notif = Column(Boolean)                # SCIZ notifs ?
    nom = Column(String(50))                    # Nom
    race = Column(String(10))                   # Race
    niv = Column(Integer)                       # Niveau
    nb_kill = Column(Integer)                   # Nombre de kills
    nb_mort = Column(Integer)                   # Nombre de morts
    nb_mouche = Column(Integer)                 # Nombre de mouches
    id_guilde = Column(Integer)                 # Numéro de guilde
    rang_guilde = Column(Integer)               # Numéro de rang dans la guilde
    etat = Column(String(50))                   # Etat
    pnj = Column(Boolean)                       # Est un PNJ ?
    ami_mh = Column(Boolean)                    # Est un ami MH ?
    inscription = Column(DateTime)              # Date d'inscription
    blason_url = Column(String(150))            # URL du blason (profil public)
    pos_x = Column(Integer)                     # Position axe X
    pos_y = Column(Integer)                     # Position axe Y
    pos_n = Column(Integer)                     # Posistion axe N
    pv = Column(Integer)                        # Nombre de points de vie restants
    bonus_pv_phy = Column(Integer)              # Bonus de PdV physique
    bonus_pv_mag = Column(Integer)              # Bonus de PdV magique
    base_pv_max = Column(Integer)               # Nombre maximum de points de vie (hors bonus)
    bonus_pv_max_phy = Column(Integer)          # Bonus de PdV max physique
    bonus_pv_max_mag = Column(Integer)          # Bonus de PdV max magique
    base_bonus_pv_max = Column(Integer)         # Nombre maximum de points de vie avec bonus
    pa = Column(Integer)                        # Nombre de points d'actions restants
    dla = Column(DateTime)                      # Horodatage de la prochaine DLA
    base_att = Column(Integer)                  # Nombre de D6 d'attaque
    bonus_att_phy = Column(Integer)             # Bonus d'attaque physique
    bonus_att_mag = Column(Integer)             # Bonus d'attaque magique
    base_esq = Column(Integer)                  # Nombre de D6 d'esquive
    bonus_esq_phy = Column(Integer)             # Bonus d'esquive physique
    bonus_esq_mag = Column(Integer)             # Bonus d'esquive magique
    base_deg = Column(Integer)                  # Nombre de D3 de dégâts
    bonus_deg_phy = Column(Integer)             # Bonus de dégâts physique
    bonus_deg_mag = Column(Integer)             # Bonus de dégâts magique
    base_reg = Column(Integer)                  # Nombre de D3 de régénération
    bonus_reg_phy = Column(Integer)             # Bonus de régénération physique
    bonus_reg_mag = Column(Integer)             # Bonus de régénération magique
    base_vue = Column(Integer)                  # Nombre de cases de vue
    bonus_vue_phy = Column(Integer)             # Bonus de vue physique
    bonus_vue_mag = Column(Integer)             # Bonus de vue magique
    base_arm_phy = Column(Integer)              # Nombre de D3 d'armure physique naturelle
    malus_base_arm_phy = Column(Integer)        # Nombre de dés d'armure en moins à ce stade du tour
    bonus_arm_phy = Column(Integer)             # Bonus d'armure physique apporté par l'équipement
    bonus_arm_mag = Column(Integer)             # Bonus d'armure magique
    base_mm = Column(Integer)                   # Nombre de points de Maitrise Magique de base
    bonus_mm_phy = Column(Integer)              # Bonus de MM physique
    bonus_mm_mag = Column(Integer)              # Bonus de MM magique
    base_rm = Column(Integer)                   # Nombre de points de Résistance Magique de base
    bonus_rm_phy = Column(Integer)              # Bonus de RM physique
    bonus_rm_mag = Column(Integer)              # Bonus de RM magique
    nb_att_sub = Column(Integer)                # Nombre d'attaques subies dans le tour
    fatigue = Column(Integer)                   # Nombre de points de fatigue actuels
    intangible = Column(Boolean)                # Est intangible ?
    camouflage = Column(Boolean)                # Est camouflé ?
    invisible = Column(Boolean)                 # Est invisible ?
    immobile = Column(Boolean)                  # Est immobilisé ?
    terre = Column(Boolean)                     # Est à terre ?
    course = Column(Boolean)                    # Est en course ?
    levite = Column(Boolean)                    # Est en lévitation ?
    nb_parade_prog = Column(Integer)            # Nombre de parades programmées
    nb_ctr_att_prog = Column(Integer)           # Nombre de contre-attaques programmées
    base_tour = Column(Integer)                 # Durée de base du tour en minutes
    bonus_tour = Column(Integer)                # Bonus de durée du tour (???)
    bonus_tour_phy = Column(Integer)            # Bonus de durée du tour physique
    bonus_tour_mag = Column(Integer)            # Bonus de durée du tour magique
    base_poids = Column(Integer)                # Poids de base en minutes
    malus_poids_phy = Column(Integer)           # Malus de poids physique
    malus_poids_mag = Column(Integer)           # Malus de poids magique
    base_concentration = Column(Integer)        # Concentration de base en %
    bonus_concentration_phy = Column(Integer)   # Bonus de concentration physique en %
    bonus_concentration_mag = Column(Integer)   # Bonus de concentration magique en %
    pi = Column(Integer)                        # Nombre de PI totaux
    limite_vue = Column(Integer)                # Limite effective de la vue
    nb_retraite_prog = Column(Integer)          # Nombre de retraite programmées
    dir_retraite = Column(String(10))           # Direction des retraites par ordre chronologique

    # Relationships
    cdms = relationship('CDM', back_populates='troll')
    user = relationship('USER', back_populates='troll', uselist=False)
    att_events = relationship('BATTLE_EVENT', foreign_keys='[BATTLE_EVENT.att_troll_id]',back_populates='att_troll')
    def_events = relationship('BATTLE_EVENT', foreign_keys='[BATTLE_EVENT.def_troll_id]',back_populates='def_troll')
    
    # Constructor
    # Handled by SqlAlchemy, accept keywords names matching the mapped columns, do not override

    def update_from_new(self, troll):
        lst = ['pv']
        if self.nom == None: # Update the name of the troll only if not known so far (on the fly troll adding case)
            lst.append('nom')
        sg.copy_properties(troll, self, lst, False)

    # Generate the string representation of each attribute and return the list of attributes printable
    def stringify(self):
        # Generate STR representation
        # TODO: only use s_ attr for pprinter (based on confs/sciz.ini)? Then this will be useful
        #plain_attrs = ['pv','niv']
        #for attr in plain_attrs:
        #    val = getattr(self, attr)
        #    setattr(self, 's_' + attr, val)
        if self.dla != None:
            self.s_dla = sg.format_time(self.dla)


