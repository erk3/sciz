#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import re, datetime, ConfigParser
import modules.globals as sg

# Class of an Identification Des Champignons
class IDC(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'idcs'
    __table_args__ = (PrimaryKeyConstraint('id', 'group_id'), )
    # Identifiant unique
    id = Column(Integer, autoincrement=True)
    # ID du champignon
    champi_id = Column(Integer)#, ForeignKey('champis.id', ondelete="CASCADE"))
    # Date de création
    time = Column(DateTime())
    # ID du troll
    troll_id = Column(Integer, ForeignKey('trolls.id', ondelete="CASCADE"))
    # ID du groupe d'appartenance
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    # Type du champignon
    type = Column(String(50))
    # Qualité du champignon
    qualite = Column(String(50))
    # Pos X du champignon
    posx = Column(Integer)
    # Pos Y du champignon
    posy = Column(Integer)
    # Pos N du champignon
    posn = Column(Integer)

    # Associations One-To-Many
    group = relationship("GROUP", back_populates="idcs")
    troll = relationship("TROLL", primaryjoin="and_(IDC.troll_id==TROLL.id, IDC.group_id==TROLL.group_id)", back_populates="idcs")
    # Associations One-To-One
    event = relationship('EVENT', primaryjoin="and_(IDC.id==EVENT.idc_id, IDC.group_id==EVENT.group_id)", back_populates='idc', uselist=False)

    # Constructor is handled by SqlAlchemy, do not override

    # Additional build logic (see MailParser)
    def build(self):
        self.time = datetime.datetime.strptime(self.time, '%d/%m/%Y  %H:%M:%S')

    def stringify(self, reprs, short, attrs):
        # Build the string representations provided
        for (key, value) in reprs:
            s = ''
            try:
                if key.startswith('s_'):
                    setattr(self, key, value)
                    continue
                elif hasattr(self, key) and getattr(self, key) is not None and (not isinstance(getattr(self, key), bool) or getattr(self, key)):
                    s = value.format(getattr(self, key))
            except KeyError as e:
                pass
            setattr(self, 's_' + key, s)
        # Add the time
        self.s_time = sg.format_time(self.time, self.s_time)
        # Add the troll name
        self.s_nom_full = self.troll.stringify_name()
        # Compute some additional things
        self.s_pos = self.s_pos.format(o=self) if self.s_posx != '' else ''
        # Return the final formated representation
        if short:
            res = self.s_short
        else:
            res = self.s_long
        res = res.format(o=self)
        res = re.sub(r'None', '', res)
        res = re.sub(r' +', ' ', res)
        return res

    def __getattr__(self, name):
        if hasattr(self, name) or name.startswith('_'):
            return super(PORTAL, self).__getattribute__(name)
        else:
            return None # Trick for the stringify logic (avoiding the raise of an error)
