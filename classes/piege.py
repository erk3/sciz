#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import re, datetime, ConfigParser
import modules.globals as sg

# Class of a Piege
class PIEGE(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'pieges'
    __table_args__ = (PrimaryKeyConstraint('id', 'group_id'), )
    # Identifiant unique
    id = Column(Integer, autoincrement=True)
    # Date de création
    time = Column(DateTime())
    # Type (Glue / Feu)
    type = Column(String(50))
    # ID du troll
    troll_id = Column(Integer, ForeignKey('trolls.id'))
    # ID du groupe d'appartenance
    group_id = Column(Integer, ForeignKey('groups.id'))
    # Pos X du piège
    posx = Column(Integer)
    # Pos Y du piège    
    posy = Column(Integer)
    # Pos N du piège
    posn = Column(Integer)
    # Maitrise Magique du piège
    mm = Column(Integer)

    # Associations One-To-Many
    group = relationship("GROUP", back_populates="pieges")
    troll = relationship("TROLL", primaryjoin="and_(PIEGE.troll_id==TROLL.id, PIEGE.group_id==TROLL.group_id)", back_populates="pieges")
    # Associations Many-To-One
    battles = relationship('BATTLE', primaryjoin="and_(PIEGE.id==BATTLE.piege_id, PIEGE.group_id==BATTLE.group_id)", back_populates='piege')
    # Associations One-To-One
    event = relationship('EVENT', primaryjoin="and_(PIEGE.id==EVENT.piege_id, PIEGE.group_id==EVENT.group_id)", back_populates='piege', uselist=False)

    # Constructor is handled by SqlAlchemy, do not override

    def populate_from_mail(self, subject, body, group):
        try:
            re_event_troll = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_EVENT_TROLL_RE)
            re_event_time = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_EVENT_TIME_RE)
            re_piege_desc = sg.config.get(sg.CONF_PIEGE_SECTION, sg.CONF_PIEGE_DESC_RE)
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
