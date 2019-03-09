#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from sqlalchemy import event, Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
import re
import modules.globals as sg


# CLASS DEFINITION
class Being(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Identifier
    id = Column(Integer, primary_key=True)
    # Name
    nom = Column(String(100))
    # Kind of being
    type = Column(String(50))

    # SQL Table Mapping
    __tablename__ = 'being'
    __mapper_args__ = {
        'polymorphic_identity': 'Créature',
        'polymorphic_on': type,
    }

    @hybrid_property
    def is_mob(self):
        return int(self.id) > 300000

    @staticmethod
    def is_mob(oid):
        return int(oid) > 300000

    @staticmethod
    def parse_name(oid, nom):
        if oid is None or nom is None:
            return ''
        if int(oid) > 300000:
            res = re.search('(((?P<mob_det>une?)\s+)?(?P<mob_nom>.+)\s+\[(?P<mob_age>.+)\]\s*(?P<mob_tag>.+)?)(?s)', nom)
            if res is not None:
                mob_nom = re.sub('\s+', ' ', res.groupdict()['mob_nom']).strip()
                mob_age = re.sub('\s+', ' ', res.groupdict()['mob_age']).strip()
                mob_tag = re.sub('\s+', ' ', res.groupdict()['mob_tag']).strip() if res.groupdict()['mob_tag'] is not None else ''
                return mob_nom.strip(), mob_age, mob_tag
        return re.sub('\s+', ' ', nom).strip(), None, None


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(Being, 'before_insert', propagate=True)
@event.listens_for(Being, 'before_update', propagate=True)
def parse_name(mapper, connection, target):
    nom, age, tag = Being.parse_name(target.id, target.nom)
    if nom is not None: target.nom = nom
    if age is not None: target.age = age
    if tag is not None: target.tag = tag
