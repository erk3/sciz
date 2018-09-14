#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import re, datetime, ConfigParser
import modules.globals as sg

# Class of a Lieu
class LIEU(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'lieux'
    __table_args__ = (PrimaryKeyConstraint('id'), )
    # Identifiant unique
    id = Column(Integer, autoincrement=True)
    # Nom du lieu
    nom = Column(String(50))
    # Pos X du lieu
    pos_x = Column(Integer)
    # Pos Y du lieu
    pos_y = Column(Integer)
    # Pos N du lieu
    pos_n = Column(Integer)

    # Constructor is handled by SqlAlchemy, do not override

    # Additional build logic (see MailParser)
    def build(self):
        pass

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
        # Compute some additional things
        self.s_pos = self.s_pos.format(o=self)
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
            return super(LIEU, self).__getattribute__(name)
        else:
            return None # Trick for the stringify logic (avoiding the raise of an error)
