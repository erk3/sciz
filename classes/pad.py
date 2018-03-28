#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a Configuration item
class PAD(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'pads'
    __table_args__ = (UniqueConstraint('group_id'), )
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    value = Column(Text)
    
    # Associations One-To-One
    group = relationship("GROUP", back_populates="pad", uselist=False)

    # Constructor is handled by SqlAlchemy do not override
