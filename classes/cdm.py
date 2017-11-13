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
    group_id = Column(Integer, ForeignKey('groups.id'))
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
    
    # Populate object from a mail and the dedicated regexp in the configuration file
    def populate_from_mail(self, subject, body, group):
        # Load the regexp
        try:
            re_event_troll = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_EVENT_TROLL_RE)
            re_event_time = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_EVENT_TIME_RE)
            re_cdm_desc = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_DESC_RE)
            re_cdm_type = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_TYPE_RE)
            re_cdm_niv = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_NIV_RE)
            re_cdm_blessure = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_BLESSURE_RE)
            re_cdm_pv = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_PV_RE)
            re_cdm_att = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_ATT_RE)
            re_cdm_esq = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_ESQ_RE)
            re_cdm_deg = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_DEG_RE)
            re_cdm_reg = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_REG_RE)
            re_cdm_arm = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_ARM_RE)
            re_cdm_vue = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_VUE_RE)
            re_cdm_mm = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_MM_RE)
            re_cdm_rm = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_RM_RE)
            re_cdm_capa = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_CAPA_RE)
            re_cdm_nb_att = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_NB_ATT_RE)
            re_cdm_vit_dep = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_VIT_DEP_RE)
            re_cdm_vlc = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_VLC_RE)
            re_cdm_att_dist = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_ATT_DIST_RE)
            re_cdm_dla = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_DLA_RE)
            re_cdm_tour = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_TOUR_RE)
            re_cdm_chargement = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_CHARGEMENT_RE)
            re_cdm_bonus_malus = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_BONUS_MALUS_RE)
            re_cdm_portee_capa = sg.config.get(sg.CONF_CDM_SECTION, sg.CONF_CDM_PORTEE_CAPA_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # GROUP
        self.group_id = group.id
        # Event Troll
        res = re.search(re_event_troll, body)
        self.troll_id = res.group(1)
        # Event time
        res = re.search(re_event_time, body)
        self.time = datetime.datetime.strptime(res.group(1), '%d/%m/%Y  %H:%M:%S')
        # CDM level and mob id
        res = re.search(re_cdm_desc, subject)
        self.comp_niv = res.group(3)
        self.mob_name = res.group(4)
        self.mob_age = res.group(5)
        self.mob_tag = res.group(6) or None
        self.mob_id = res.group(7)
        # Mob Type
        res = re.search(re_cdm_type, body)
        self.type = res.group(1)
        # Mob Blessure
        res = re.search(re_cdm_blessure, body)
        self.blessure = res.group(1)
        # Mob min/max level
        res = re.search(re_cdm_niv, body)
        self.niv_min = res.group(2) or (res.group(4) or (res.group(6) or None))
        self.niv_max = res.group(3) or (res.group(5) or (res.group(6) or None))
        # Mob min/max pv
        res = re.search(re_cdm_pv, body)
        self.pv_min = res.group(2) or (res.group(4) or (res.group(6) or None))
        self.pv_max = res.group(3) or (res.group(5) or (res.group(6) or None))
        # Mob min/max att
        res = re.search(re_cdm_att, body)
        self.att_min = res.group(2) or (res.group(4) or (res.group(6) or None))
        self.att_max = res.group(3) or (res.group(5) or (res.group(6) or None))
        # Mob min/max esq
        res = re.search(re_cdm_esq, body)
        self.esq_min = res.group(2) or (res.group(4) or (res.group(6) or None))
        self.esq_max = res.group(3) or (res.group(5) or (res.group(6) or None))
        # Mob min/max deg
        res = re.search(re_cdm_deg, body)
        self.deg_min = res.group(2) or (res.group(4) or (res.group(6) or None))
        self.deg_max = res.group(3) or (res.group(5) or (res.group(6) or None))
        # Mob min/max reg
        res = re.search(re_cdm_reg, body)
        self.reg_min = res.group(2) or (res.group(4) or (res.group(6) or None))
        self.reg_max = res.group(3) or (res.group(5) or (res.group(6) or None))
        # Mob min/max arm_phy
        res = re.search(re_cdm_arm, body)
        self.arm_phy_min = res.group(2) or (res.group(4) or (res.group(6) or None))
        self.arm_phy_max = res.group(3) or (res.group(5) or (res.group(6) or None))
        # Mob min/max vue
        res = re.search(re_cdm_vue, body)
        self.vue_min = res.group(2) or (res.group(4) or (res.group(6) or None))
        self.vue_max = res.group(3) or (res.group(5) or (res.group(6) or None))
        # Mob min/max mm
        res = re.search(re_cdm_mm, body)
        if res:
            self.mm_min = res.group(2) or (res.group(4) or (res.group(6) or None))
            self.mm_max = res.group(3) or (res.group(5) or (res.group(6) or None))
        # Mob min/max rm
        res = re.search(re_cdm_rm, body)
        if res:
            self.rm_min = res.group(2) or (res.group(4) or (res.group(6) or None))
            self.rm_max = res.group(3) or (res.group(5) or (res.group(6) or None))
        # Mob Capa
        res = re.search(re_cdm_capa, body, re.DOTALL)
        if res:
            self.capa_desc = res.group(1)
            self.capa_effet = re.sub(r'((<br>)?\n|\|)$', '', res.group(3))
            self.capa_tour = res.group(5)
        # Mob nb att
        res = re.search(re_cdm_nb_att, body)
        if res: self.nb_att_tour = res.group(1)
        # Mob vit_dep
        res = re.search(re_cdm_vit_dep, body)
        if res: self.vit_dep = res.group(1)
        # Mob vlc
        res = re.search(re_cdm_vlc, body)
        if res: self.vlc = sg.parseFrenchBoolean(res.group(1))
        # Mob att_dist
        res = re.search(re_cdm_att_dist, body)
        if res: self.att_dist = sg.parseFrenchBoolean(res.group(1))
        # Mob dla
        res = re.search(re_cdm_dla, body)
        if res: self.dla = res.group(1)
        # Mob min/max tour
        res = re.search(re_cdm_tour, body)
        if res:
            self.tour_min = res.group(2) or (res.group(4) or (res.group(6) or None))
            self.tour_max = res.group(3) or (res.group(5) or (res.group(6) or None))
        # Mob chargement
        res = re.search(re_cdm_chargement, body)
        if res: self.chargement = res.group(1)
        # Mob bonus/malus
        res = re.search(re_cdm_bonus_malus, body)
        if res: self.bonus_malus = res.group(1)
        # Mob portée Capa
        res = re.search(re_cdm_portee_capa, body)
        if res: self.portee_capa = res.group(1)

    # Generate the string representation of each attribute and return the list of attributes printable
    def stringify(self):
        # Generate STR representation
        self.troll.stringify();
        self.s_tag = ' ' + self.mob.tag if self.mob.tag else ''
        self.s_nom_short = self.mob.nom + ' (' + str(self.mob.id) + ')'
        self.s_nom_full = self.mob.nom + ' [' + self.mob.age + ']' + self.s_tag + ' (' + str(self.mob.id) + ')'
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
