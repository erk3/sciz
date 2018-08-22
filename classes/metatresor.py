#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a MetaTresor (from MH FTP)
class METATRESOR(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'metatresors'
    # ID unique du metatresor
    id = Column(Integer, primary_key=True)
    # Nom (sans modificateur)
    nom = Column(String(50))
    # Type
    type = Column(String(50))
    
    # Associations Many-To-One
    idts = relationship("IDT", back_populates="metatresor")

    # Constructor is handled by SqlAlchemy, do not override
