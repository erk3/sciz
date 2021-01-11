#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from sqlalchemy import Column, Integer, String
import modules.globals as sg


# CLASS DEFINITION
class MetaCapa(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier (negative for skills, positive for spells)
    id = Column(Integer, primary_key=True)
    # Name
    nom = Column(String(50))
    # Type
    type = Column(String(50))
    # Subtype
    subtype = Column(String(50))
    # PA
    pa = Column(Integer)

    # SQL Table Mapping
    __tablename__ = 'capa_meta'

    @staticmethod
    def find_by_name(nom):
        # Loop over every metamobs to find the longest one matching the mob name
        capas = sg.db.session.query(MetaCapa).all()
        res = None
        for capa in capas:
            if capa.nom.lower() in nom.lower():
                res = capa
                break
        return res
