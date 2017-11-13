#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a Configuration item
class CONF(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'confs'
    __table_args__ = (UniqueConstraint('group_id', 'key'), )
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    key = Column(String(50))
    value = Column(String(255))
    last_fetch = Column(DateTime, onupdate=datetime.datetime.utcnow())
    
    # Associations One-To-Many
    group = relationship("GROUP", back_populates="confs")

    # Constructor is handled by SqlAlchemy do not override

    def touch(self):
        self.last_fetch = datetime.datetime.utcnow()
