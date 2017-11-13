#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a MetaMob (from MH FTP)
class METAMOB(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'metamobs'
    # ID unique du metamonstre
    id = Column(Integer, primary_key=True)
    # Nom (sans modificateur)
    nom = Column(String(50))
    # Déterminant du monstre
    determinant = Column(String(10))
    # URL du blason
    blason_url = Column(String(150))
    
    # Associations Many-To-One
    mobs = relationship("MOB", back_populates="metamob")

    # Constructor is handled by SqlAlchemy, do not override
