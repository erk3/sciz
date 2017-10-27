#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import re, datetime, ConfigParser
import modules.globals as sg

# Class of a Notification
class PIEGE(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'pieges'
    id = Column(Integer, primary_key=True)                  # Identifiant unique
    time = Column(DateTime())                               # Date de création
    type = Column(String(50))                               # Type (Glue / Feu)
    troll_id = Column(Integer, ForeignKey('trolls.id'))     # ID du troll
    battle_event_id = Column(Integer, ForeignKey('battle_events.id'))   # ID de l'évènement de déclenchement
    posx = Column(Integer)                                  # Pos X du piège
    posy = Column(Integer)                                  # Pos Y du piège    
    posn = Column(Integer)                                  # Pos N du piège
    mm = Column(Integer)                                    # Maitrise Magique du piège

    # Associations
    troll = relationship("TROLL", back_populates="pieges")
    battle_event = relationship('BATTLE_EVENT', foreign_keys=[battle_event_id], back_populates='piege', uselist=False)
    event = relationship('EVENT', back_populates='piege', uselist=False)

    # Constructor
    # Handled by SqlAlchemy, accept keywords names matching the mapped columns, do not override

    def populate_from_mail(self, subject, body, config, logger):
        try:
            re_event_troll = config.get(sg.CONF_MAIL_SECTION, sg.CONF_EVENT_TROLL_RE)
            re_event_time = config.get(sg.CONF_MAIL_SECTION, sg.CONF_EVENT_TIME_RE)
            re_piege_desc = config.get(sg.CONF_PIEGE_SECTION, sg.CONF_PIEGE_DESC_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            logger.error("Fail to load config! (ConfigParser error:" + str(e) + ")")
            raise
        # Event Troll
        res = re.search(re_event_troll, body)
        self.troll_id = res.group(1)
        # Event time
        res = re.search(re_event_time, body)
        self.time = datetime.datetime.strptime(res.group(1), '%d/%m/%Y  %H:%M:%S')
        # Piege
        res = re.search(re_piege_desc, body)
        self.type = res.group(1)
        self.posx = res.group(2)
        self.posy = res.group(3)
        self.posn = res.group(4)
        self.mm = res.group(5)

    # Generate the string representation of each attribute and return the list of attributes printable
    def stringify(self):
        # Generate STR representation
        self.troll.stringify();
