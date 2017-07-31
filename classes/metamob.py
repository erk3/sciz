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
    id = Column(Integer, primary_key=True)              # Identifiant unique du monstre
    nom = Column(String(50))                            # Nom (sans modificateur)
    determinant = Column(String(10))                    # Déterminant du monstre
    blason_url = Column(String(150))                    # URL du blason
    
    mobs = relationship("MOB", back_populates="metamob")

    # Constructor
    # Handled by SqlAlchemy, accept keywords names matching the mapped columns, do not override
