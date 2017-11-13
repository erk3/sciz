#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import re, datetime, ConfigParser, copy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a Battle
class BATTLE(sg.SqlAlchemyBase):
    
    # SQL Table Mapping
    __tablename__ = 'battles'
    __table_args__ = (PrimaryKeyConstraint('id', 'group_id'), )
    # ID unique
    id = Column(Integer, autoincrement=True)
    # Horodatage de l'event
    time = Column(DateTime)
    # ID du troll attaquant
    att_troll_id = Column(Integer, ForeignKey('trolls.id'))
    # ID du troll défenseur
    def_troll_id = Column(Integer, ForeignKey('trolls.id'))
    # ID du monstre attaquant
    att_mob_id = Column(Integer, ForeignKey('mobs.id'))
    # ID du monstre défenseur
    def_mob_id = Column(Integer, ForeignKey('mobs.id'))
    # ID du piège
    piege_id = Column(Integer, ForeignKey('pieges.id'))
    # ID du groupe
    group_id = Column(Integer, ForeignKey('groups.id'))
    # FLAG (ATT, DEF, HYPNO, SACRO...)
    flag_type = Column(String(50))
    # Type d'évènement
    type = Column(String(50))
    # Sous type d'évènement
    subtype = Column(String(50))
    # Jet d'attaque
    att = Column(Integer)
    # Jet d'esquive
    esq = Column(Integer)
    # Jet de dégâts (sans compter armure)
    deg = Column(Integer)
    # Points de vie perdu par la cible (avec armure)
    pv = Column(Integer)
    # Points de vie restants de la cible
    vie = Column(Integer)
    # Points de vie rendu à la cible
    soin = Column(Integer)
    # Blessure infligée à l'attaquant
    blessure = Column(Integer)
    # Seuil de résistance en %
    sr = Column(Integer)
    # Jet de résistance en %
    resi = Column(Integer)
    # Descritpion de la capacité spéciale
    capa_desc = Column(String(150))
    # Effet de la capacité spéciale
    capa_effet = Column(String(150))
    # Nombre de tours d'effet de la capacité spéciale
    capa_tour = Column(Integer)

    # Associations One-To-Many
    att_troll = relationship("TROLL", primaryjoin="and_(BATTLE.att_troll_id==TROLL.id, BATTLE.group_id==TROLL.group_id)", back_populates="atts")
    def_troll = relationship("TROLL", primaryjoin="and_(BATTLE.def_troll_id==TROLL.id, BATTLE.group_id==TROLL.group_id)", back_populates="defs")
    att_mob = relationship("MOB", primaryjoin="and_(BATTLE.att_mob_id==MOB.id, BATTLE.group_id==MOB.group_id)", back_populates="atts")
    def_mob = relationship("MOB", primaryjoin="and_(BATTLE.def_mob_id==MOB.id, BATTLE.group_id==MOB.group_id)", back_populates="defs")
    piege = relationship("PIEGE", primaryjoin="and_(BATTLE.piege_id==PIEGE.id, BATTLE.group_id==PIEGE.group_id)", back_populates="battles")
    group = relationship("GROUP", back_populates="battles")
    # Associations One-To-One
    event = relationship("EVENT", primaryjoin="and_(BATTLE.id==EVENT.battle_id, BATTLE.group_id==EVENT.group_id)", back_populates="battle", uselist=False)

    # Constructor is handled by SqlAlchemy do not override
    
    # Populate object from a mail and the dedicated regexp in the configuration file
    def populate_from_mail(self, subject, body, group, flag_type):
        # Load the regexp
        try:
            re_event_troll = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_EVENT_TROLL_RE)
            re_event_type = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_EVENT_TYPE_RE)
            re_event_time = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_EVENT_TIME_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # FLAG
        self.flag_type = flag_type
        # GROUP
        self.group_id = group.id
        # Event Troll
        res = re.search(re_event_troll, body)
        if 'ATT' in flag_type:
            self.att_troll_id = res.group(1)
            self.att_troll_nom = res.group(2)
        elif 'DEF' in flag_type:
            self.def_troll_id = res.group(1)
            self.def_troll_nom = res.group(2)
        # Event time
        res = re.search(re_event_time, body)
        self.time = datetime.datetime.strptime(res.group(1), '%d/%m/%Y  %H:%M:%S')
        # Dispatch
        if flag_type == 'ATT':
            self.__populate_from_att_mail(subject, body)
        elif flag_type == 'DEF':
            self.__populate_from_def_mail(subject, body)
        elif flag_type == 'ATT HYPNO':
            self.__populate_from_att_hypno_mail(subject, body)
        elif flag_type == 'DEF HYPNO':
            self.__populate_from_def_hypno_mail(subject, body)
        elif flag_type == 'ATT SACRO':
            self.__populate_from_att_sacro_mail(subject, body)
        elif flag_type == 'DEF SACRO':
            self.__populate_from_def_sacro_mail(subject, body)
        elif flag_type == 'ATT VT':
            self.__populate_from_att_vt_mail(subject, body)
        elif flag_type == 'DEF VT':
            self.__populate_from_def_vt_mail(subject, body)
        elif flag_type == 'ATT EXPLO':
            return self.__populate_from_att_explo_mail(subject, body)
        elif flag_type == 'DEF EXPLO':
            self.__populate_from_def_explo_mail(subject, body)
        elif flag_type == 'DEF CAPA':
            self.__populate_from_capa_mail(subject, body)
        else:
            # Should never happen
            sg.logger.warning('Unrecognized flag %s, mail not handled properly' %s (flag_type, ))

    def __populate_from_att_mail(self, subject, body):   
        # Load config
        try:
            re_event_desc = sg.config.get(sg.CONF_ATT_SECTION, sg.CONF_EVENT_DESC_RE)
            re_event_att = sg.config.get(sg.CONF_ATT_SECTION, sg.CONF_EVENT_ATT_RE)
            re_event_esq = sg.config.get(sg.CONF_ATT_SECTION, sg.CONF_EVENT_ESQ_RE)
            re_event_deg = sg.config.get(sg.CONF_ATT_SECTION, sg.CONF_EVENT_DEG_RE)
            re_event_pv = sg.config.get(sg.CONF_ATT_SECTION, sg.CONF_EVENT_PV_RE)
            re_event_sr = sg.config.get(sg.CONF_ATT_SECTION, sg.CONF_EVENT_SR_RE)
            re_event_resi = sg.config.get(sg.CONF_ATT_SECTION, sg.CONF_EVENT_RESI_ATT_RE)
            re_event_soin_att = sg.config.get(sg.CONF_ATT_SECTION, sg.CONF_EVENT_SOIN_ATT_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # Event desc
        res = re.search(re_event_desc, subject)
        self.type = res.group(2)
        self.subtype = res.group(3)
        if res.group(4) == None: # Trick matching the det (only mobs have it)
            self.def_troll_nom = res.group(5)
            self.def_troll_id = res.group(10)
        else:
            self.def_mob_nom = res.group(5)
            self.def_mob_age = res.group(7)
            self.def_mob_tag = res.group(9)
            self.def_mob_id = res.group(10)
        # Jet d'attaque
        res = re.search(re_event_att, body)
        self.att = res.group(1) if res else None
        # Jet d'esquive
        res = re.search(re_event_esq, body)
        self.esq = res.group(1) if res else None
        # Seuil de résistance
        res = re.search(re_event_sr, body)
        self.sr = res.group(1) if res else None
        # Jet de résistance
        res = re.search(re_event_resi, body)
        self.resi = res.group(1) if res else None
        # Jet de dégâts
        res = re.search(re_event_deg, body)
        self.deg = res.group(1) if res else None
        # Points de vie récupérés (Vampirisme)
        res = re.search(re_event_soin_att, body)
        self.soin = res.group(1) if res else None
        # Points de vie perdus
        res = re.search(re_event_pv, body)
        self.pv = res.group(1) if res else self.deg # Pas d'armure
    
    def __populate_from_def_mail(self, subject, body):       
        # Load config
        try:
            re_event_desc = sg.config.get(sg.CONF_DEF_SECTION, sg.CONF_EVENT_DESC_RE)
            re_event_att = sg.config.get(sg.CONF_DEF_SECTION, sg.CONF_EVENT_ATT_RE)
            re_event_esq = sg.config.get(sg.CONF_DEF_SECTION, sg.CONF_EVENT_ESQ_RE)
            re_event_deg = sg.config.get(sg.CONF_DEF_SECTION, sg.CONF_EVENT_DEG_RE)
            re_event_pv = sg.config.get(sg.CONF_DEF_SECTION, sg.CONF_EVENT_PV_RE)
            re_event_vie = sg.config.get(sg.CONF_DEF_SECTION, sg.CONF_EVENT_VIE_RE)
            re_event_capa = sg.config.get(sg.CONF_DEF_SECTION, sg.CONF_EVENT_CAPA_RE)
            re_event_capa_effet_def = sg.config.get(sg.CONF_DEF_SECTION, sg.CONF_EVENT_CAPA_EFFET_DEF_RE)
            re_event_capa_tour = sg.config.get(sg.CONF_DEF_SECTION, sg.CONF_EVENT_CAPA_TOUR_RE)
            re_event_sr = sg.config.get(sg.CONF_DEF_SECTION, sg.CONF_EVENT_SR_RE)
            re_event_resi = sg.config.get(sg.CONF_DEF_SECTION, sg.CONF_EVENT_RESI_DEF_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # Event desc
        res = re.search(re_event_desc, subject)
        self.type = res.group(2)
        if res.group(3) == 'de': # Trick matching the det
            self.att_troll_nom = res.group(4)
            self.att_troll_id = res.group(9)
        else:
            self.att_mob_nom = res.group(4)
            self.att_mob_age = res.group(6)
            self.att_mob_tag = res.group(8)
            self.att_mob_id = res.group(9)
        # Jet d'attaque
        res = re.search(re_event_att, body)
        self.att = res.group(1) if res else None
        # Jet d'esquive
        res = re.search(re_event_esq, body)
        self.esq = res.group(1) if res else None
        # Seuil de résistance
        res = re.search(re_event_sr, body)
        self.sr = res.group(1) if res else None
        # Jet de résistance
        res = re.search(re_event_resi, body)
        self.resi = res.group(1) if res else None
        # Jet de dégâts
        res = re.search(re_event_deg, body)
        self.deg = res.group(1) if res else None
        # Points de vie perdus
        res = re.search(re_event_pv, body)
        self.pv = res.group(1) if res else self.deg # Pas d'armure
        # Points de vie restants
        res = re.search(re_event_vie, body)
        self.vie = res.group(1) if res else None
        # Capa desc
        res = re.search(re_event_capa, body)
        self.capa_desc = res.group(1) if res else None
        # Capa effet
        res = re.search(re_event_capa_effet_def, body)
        self.capa_effet = res.group(2) if res else None
        # Capa tour
        res = re.search(re_event_capa_tour, body)
        self.capa_tour = res.group(1) if res else None
        
    def __populate_from_capa_mail(self, subject, body):       
        # Load config
        try:
            re_event_pv = sg.config.get(sg.CONF_CAPA_SECTION, sg.CONF_EVENT_PV_RE)
            re_event_vie = sg.config.get(sg.CONF_CAPA_SECTION, sg.CONF_EVENT_VIE_RE)
            re_event_capa = sg.config.get(sg.CONF_CAPA_SECTION, sg.CONF_EVENT_CAPA_RE)
            re_event_capa_effet_def = sg.config.get(sg.CONF_CAPA_SECTION, sg.CONF_EVENT_CAPA_EFFET_DEF_RE)
            re_event_capa_tour = sg.config.get(sg.CONF_CAPA_SECTION, sg.CONF_EVENT_CAPA_TOUR_RE)
            re_event_sr = sg.config.get(sg.CONF_CAPA_SECTION, sg.CONF_EVENT_SR_RE)
            re_event_resi = sg.config.get(sg.CONF_CAPA_SECTION, sg.CONF_EVENT_RESI_DEF_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # Event desc & Capa desc
        res = re.search(re_event_capa, body, re.M)
        self.att_mob_nom = res.group(2)
        self.att_mob_age = res.group(3)
        self.att_mob_tag = res.group(5)
        self.att_mob_id = res.group(1)
        self.capa_desc = res.group(6)
        self.type = 'Pouvoir'
        self.subtype = res.group(6)
        # Seuil de résistance
        res = re.search(re_event_sr, body, re.M)
        self.sr = res.group(1) if res else None
        # Jet de résistance
        res = re.search(re_event_resi, body, re.M)
        self.resi = res.group(1) if res else None
        # Points de vie perdus
        res = re.search(re_event_pv, body, re.M)
        self.pv = res.group(1) if res else None # Souffle / Aura de feu
        # Points de vie restants
        res = re.search(re_event_vie, body, re.M)
        self.vie = res.group(1) if res else None # Souffle / Aura de feu
        # Capa effet
        res = re.search(re_event_capa_effet_def, body, re.M)
        self.capa_effet = res.group(2) if res else None
        if res and res.group(1):
            self.type += ' résisté'
        # Capa tour
        res = re.search(re_event_capa_tour, body, re.M)
        self.capa_tour = res.group(1) if res else None
    
    def __populate_from_att_hypno_mail(self, subject, body):       
        # Load config
        try:
            re_event_desc = sg.config.get(sg.CONF_HYPNO_SECTION, sg.CONF_EVENT_DESC_RE)
            re_event_sr = sg.config.get(sg.CONF_HYPNO_SECTION, sg.CONF_EVENT_SR_RE)
            re_event_resi_att = sg.config.get(sg.CONF_HYPNO_SECTION, sg.CONF_EVENT_RESI_ATT_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # Event desc
        self.type = 'Sortilège'
        self.subtype = 'Hypnotisme'
        res = re.search(re_event_desc, body)
        if res != None:
            if res.group(2) == None: # Trick matching the det (No det = Troll ?)
                self.def_troll_nom = res.group(3)
                self.def_troll_id = res.group(8)
            else:
                self.def_mob_nom = res.group(3)
                self.def_mob_age = res.group(5)
                self.def_mob_tag = res.group(7)
                self.def_mob_id = res.group(8)
            # Capa effet
            self.capa_effet = res.group(1)
            # Seuil de résistance
            res = re.search(re_event_sr, body)
            self.sr = res.group(1) if res else None
            # Jet de résistance
            res = re.search(re_event_resi_att, body)
            self.resi = res.group(1) if res else None
            if int(self.resi) <= int(self.sr):
                    self.type += ' réduit'
        else:
            sg.logger.error("Fail to parse the mail, regexp not maching")
        
    def __populate_from_def_hypno_mail(self, subject, body):       
        # Load config
        try:
            re_event_subject = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DEF_HYPNO_RE)
            re_event_resi_def = sg.config.get(sg.CONF_HYPNO_SECTION, sg.CONF_EVENT_RESI_DEF_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # Event desc
        self.type = 'Sortilège'
        self.subtype = 'Hypnotisme'
        res = re.search(re_event_subject, subject)
        if res != None:
            self.att_troll_nom = res.group(1)
            self.att_troll_id = res.group(2)
            res = re.search(re_event_resi_def, body)
            if res != None and res.group(2) == None: # Résisté
                self.type += ' résisté'
        else:
            sg.logger.error("Fail to parse the mail, rexegp not maching")

    def __populate_from_att_vt_mail(self, subject, body):       
        # Load config
        try:
            re_event_capa_effet_att = sg.config.get(sg.CONF_VT_SECTION, sg.CONF_EVENT_CAPA_EFFET_ATT_RE)
            re_event_sr = sg.config.get(sg.CONF_VT_SECTION, sg.CONF_EVENT_SR_RE)
            re_event_resi_att = sg.config.get(sg.CONF_VT_SECTION, sg.CONF_EVENT_RESI_ATT_RE)
            re_event_capa_tour = sg.config.get(sg.CONF_VT_SECTION, sg.CONF_EVENT_CAPA_TOUR_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # Event desc
        self.type = 'Sortilège'
        self.subtype = 'Vue Troublée'
        res = re.search(re_event_capa_effet_att, body)
        if res != None:
            if res.group(3) == None: # Trick matching the det (No det = Troll ?)
                self.def_troll_nom = res.group(4)
                self.def_troll_id = res.group(9)
            else:
                self.def_mob_nom = res.group(4)
                self.def_mob_age = res.group(6)
                self.def_mob_tag = res.group(8)
                self.def_mob_id = res.group(9)
            # Capa effet
            self.capa_effet = res.group(1) if res else None
            # Capa tour
            res = re.search(re_event_capa_tour, body)
            self.capa_tour = res.group(1) if res else None
            # Seuil de résistance
            res = re.search(re_event_sr, body)
            self.sr = res.group(1) if res else None
            # Jet de résistance
            res = re.search(re_event_resi_att, body)
            self.resi = res.group(1) if res else None
            if int(self.resi) <= int(self.sr):
                    self.type += ' réduit'
        else:
            sg.logger.error("Fail to parse the mail, rexegp not maching")
    
    def __populate_from_att_explo_mail(self, subject, body):       
        # Load config
        try:
            re_event_capa_effet_att = sg.config.get(sg.CONF_EXPLO_SECTION, sg.CONF_EVENT_CAPA_EFFET_ATT_RE)
            re_event_sr = sg.config.get(sg.CONF_EXPLO_SECTION, sg.CONF_EVENT_SR_RE)
            re_event_resi_att = sg.config.get(sg.CONF_EXPLO_SECTION, sg.CONF_EVENT_RESI_ATT_RE)
            re_end_mail = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_END_MAIL_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # Event desc
        self.type = 'Sortilège'
        self.subtype = 'Explosion'
        res = re.search(re_end_mail, body)
        stop_pos = res.end()
        last_match_endpos = 0
        objs = []
        p = re.compile(re_event_capa_effet_att)
        pSR = re.compile(re_event_sr)
        pRESI = re.compile(re_event_resi_att)
        res = p.search(body, last_match_endpos)
        last_match_endpos = res.end()
        while res != None and last_match_endpos < stop_pos:
            obj = copy.deepcopy(self)
            if res.group(4) == None: # Trick matching the det (No det = Troll ?)
                obj.def_troll_nom = res.group(5)
                obj.def_troll_id = res.group(10)
            else:
                obj.def_mob_nom = res.group(5)
                obj.def_mob_age = res.group(7)
                obj.def_mob_tag = res.group(9)
                obj.def_mob_id = res.group(10)
            # Capa effet
            obj.capa_effet = res.group(1) if res else None
            obj.pv = res.group(3) if res else None
            # Seuil de résistance
            resSR = pSR.search(body, last_match_endpos)
            obj.sr = resSR.group(1) if res else None
            # Jet de résistance
            resRESI = pRESI.search(body, last_match_endpos)
            obj.resi = resRESI.group(1) if res else None
            if int(obj.resi) <= int(obj.sr):
                    obj.type += ' réduit'
            objs.append(obj)
            res = p.search(body, last_match_endpos)
            if res:
                last_match_endpos = res.end()
        return objs
    
    def __populate_from_def_vt_mail(self, subject, body):       
        # Load config
        try:
            re_event_desc = sg.config.get(sg.CONF_VT_SECTION, sg.CONF_EVENT_DESC_RE)
            re_event_capa_effet_def = sg.config.get(sg.CONF_VT_SECTION, sg.CONF_EVENT_CAPA_EFFET_DEF_RE)
            re_event_capa_tour = sg.config.get(sg.CONF_VT_SECTION, sg.CONF_EVENT_CAPA_TOUR_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # Event desc
        self.type = 'Sortilège'
        self.subtype = 'Vue Troublée'
        res = re.search(re_event_desc, body)
        if res != None:
            self.att_troll_nom = res.group(1)
            self.att_troll_id = res.group(2)
            # Capa effet
            res = re.search(re_event_capa_effet_def, body)
            self.capa_effet = res.group(1) if res else None
            # Capa tour
            res = re.search(re_event_capa_tour, body)
            self.capa_tour = res.group(1) if res else None
        else:
            sg.logger.error("Fail to parse the mail, rexegp not maching")
    
    def __populate_from_def_explo_mail(self, subject, body):       
        # Load config
        try:
            re_event_desc = sg.config.get(sg.CONF_EXPLO_SECTION, sg.CONF_EVENT_DESC_RE)
            re_event_capa_effet_def = sg.config.get(sg.CONF_EXPLO_SECTION, sg.CONF_EVENT_CAPA_EFFET_DEF_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # Event desc
        self.type = 'Sortilège'
        self.subtype = 'Explosion'
        res = re.search(re_event_desc, body)
        if res != None:
            self.att_troll_nom = res.group(1)
            self.att_troll_id = res.group(2)
            # Capa effet
            res = re.search(re_event_capa_effet_def, body)
            self.capa_effet = res.group(1) if res else None
            self.pv = res.group(3) if res else None
        else:
            sg.logger.error("Fail to parse the mail, rexegp not maching")
    
    def __populate_from_att_sacro_mail(self, subject, body):       
        # Load config
        try:
            re_event_soin_att = sg.config.get(sg.CONF_SACRO_SECTION, sg.CONF_EVENT_SOIN_ATT_RE)
            re_event_blessure = sg.config.get(sg.CONF_SACRO_SECTION, sg.CONF_EVENT_BLESSURE_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # Event desc
        self.type = 'Sortilège'
        self.subtype = 'Sacrifice'
        res = re.search(re_event_soin_att, body)
        if res != None:
            # Cible
            self.def_troll_nom = res.group(1)
            self.def_troll_id = res.group(2)
            # Soin
            self.soin = res.group(3)
        else:
            sg.logger.error("Fail to parse the mail, regexp not maching")
        res = re.search(re_event_blessure, body)
        if res != None:
            self.blessure = res.group(1)
        else:
            sg.logger.error("Fail to parse the mail, regexp not maching")

    def __populate_from_def_sacro_mail(self, subject, body):       
        # Load config
        try:
            re_event_soin_def = sg.config.get(sg.CONF_SACRO_SECTION, sg.CONF_EVENT_SOIN_DEF_RE)
            re_event_desc = sg.config.get(sg.CONF_SACRO_SECTION, sg.CONF_EVENT_DESC_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise
        # Event desc
        self.type = 'Sortilège'
        self.subtype = 'Sacrifice'
        res = re.search(re_event_desc, body)
        if res != None:
            # Cible
            self.att_troll_nom = res.group(2)
            self.att_troll_id = res.group(3)
        else:
            sg.logger.error("Fail to parse the mail, regexp not maching")
        res = re.search(re_event_soin_def, body)
        if res != None:
            self.soin = res.group(1)
        else:
            sg.logger.error("Fail to parse the mail, regexp not maching")

    def stringify(self):
        self.s_flag_type = self.flag_type
        # Attaquant
        if self.att_troll:
            self.s_att_nom = self.att_troll.nom + ' (' + str(self.att_troll.id) + ')'
            if self.att_troll.user:
                self.s_att_nom = self.att_troll.user.pseudo
        else:
            self.s_att_nom = self.att_mob.nom + ' [' + self.att_mob.age + '] (' + str(self.att_mob.id) + ')'
        # Défenseur
        if self.def_troll:
            self.s_def_nom = self.def_troll.nom + ' (' + str(self.def_troll.id) + ')'
            if self.def_troll.user:
                self.s_def_nom = self.def_troll.user.pseudo
        else:
            self.s_def_nom = self.def_mob.nom + ' [' + self.def_mob.age + '] (' + str(self.def_mob.id) + ')'
        # Capa
        self.s_capa = ''
        self.s_capa += self.capa_desc + ' ;' if self.capa_desc != None else ''
        self.s_capa += ' ' + self.capa_effet if self.capa_effet != None else ''
        self.s_capa += ' ' + str(self.capa_tour) + 'T' if self.capa_tour != None else ''
        self.s_capa = '(' + self.s_capa.lstrip() + ')' if (self.s_capa != '' and (self.pv != None or u"esquivée" in self.type or u"CAPA" in self.flag_type)) else self.s_capa.lstrip()
        self.s_capa = ' ' + self.s_capa if self.s_capa != '' else ''
        # Stats
        self.s_pv = '-' + (str(self.pv) if self.pv != None else '0')
        self.s_pv += ' (' + str(self.vie) + ' PV)' if self.vie != None else ''
        self.s_def_stats = ''
        self.s_def_stats += ' esq ' + str(self.esq) if self.esq else ''
        self.s_def_stats += ' sr ' + str(self.sr) if self.sr else ''
        self.s_def_stats = self.s_def_stats.lstrip()
        self.s_att_stats = ''
        self.s_att_stats += ' att ' + str(self.att) if self.att else ''
        self.s_att_stats += ' resi ' + str(self.resi) if self.resi else ''
        self.s_att_stats += ' deg ' + str(self.deg) if self.deg else ''
        self.s_att_stats += ' soin ' + str(self.soin) if self.soin else ''
        self.s_att_stats = self.s_att_stats.lstrip()
        # Type desc
        self.s_type_short = ''
        self.s_type = ''
        if self.flag_type == 'ATT' or self.flag_type == 'DEF':
            if "mortelle" in self.type:
                self.s_flag_type += ' (MORT)'
            self.s_type = self.type if self.type else ''
            self.s_type += ' ' + self.subtype if self.subtype else ''
        elif 'HYPNO' in self.flag_type:
            if self.type == u"Sortilège": # pas réduit/résisté
                self.s_hypno_flag = '(FULL)'
            else:
                self.s_hypno_flag = '(REDUIT)'

