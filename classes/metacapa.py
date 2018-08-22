#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a MetaCapa (Sorts/Compétences) (from MH FTP)
class METACAPA(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'metacapas'
    # ID unique de la métacapacité (Les sorts devraient avoir un ID négatif et les compétences un ID positif, voir MH_CALLER)
    id = Column(Integer, primary_key=True)
    # Type
    type = Column(String(50))
    # Nom
    nom = Column(String(50))
    # Subtype
    subtype = Column(String(50))
    # PA
    pa = Column(Integer)
    
    # Associations Many-To-Many
    trolls = relationship('AssocTrollsCapas', back_populates='metacapa')

    # Constructor is handled by SqlAlchemy, do not override
