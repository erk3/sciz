#!/usr/bin/env python3
#coding: utf-8

# IMPORTS
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import re, modules.globals as sg


# CLASS DEFINITION
class MetaTresor(sg.sqlalchemybase):

    # To pull data from MH, only useful for the name/type association and the name/templates split

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, primary_key=True)
    # Name
    nom = Column(String(50))
    # Type
    type = Column(String(50))

    # Associations
    tresor_privates = relationship('TresorPrivate', back_populates='tresor_meta', primaryjoin='MetaTresor.id == TresorPrivate.metatresor_id')

    # SQL Table Mapping
    __tablename__ = 'tresor_meta'

    @staticmethod
    def link_metatresor(tresor):
        # Dirty hardcoded fix for spells, oghams and runes...
        if tresor.nom is not None and any(a in tresor.nom.lower() for a in ['sortilège', 'ogham', 'rune :']):
            meta = sg.db.session.query(MetaTresor).filter(MetaTresor.nom == 'Sortilège').one()
            return meta.id, tresor.nom, '', meta.type
        # Loop over every metatresors to find the longest one matching the tresor name
        res_meta_id = None
        res_nom = tresor.nom
        temp_nom = tresor.nom
        res_templates = tresor.templates
        res_type = tresor.tresor_type if hasattr(tresor, 'tresor_type') else None
        if tresor.nom is not None:
            metatresors = sg.db.session.query(MetaTresor).all()
            len_found_metatresor_nom = 0
            for metatresor in metatresors:
                len_metatresor_nom = len(metatresor.nom)
                if metatresor.nom.lower() in temp_nom.lower() and len_metatresor_nom >= len_found_metatresor_nom:
                    len_found_metatresor_nom = len_metatresor_nom
                    res_meta_id = metatresor.id
                    res_nom = metatresor.nom
                    res_type = metatresor.type
                    # Split name and templates
                    if len_metatresor_nom < len(temp_nom):
                        res_templates = re.sub(metatresor.nom, '', temp_nom)
        return res_meta_id, res_nom, res_templates, res_type
