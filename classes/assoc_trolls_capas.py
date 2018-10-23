#!/usr/bin/env python
#-*- coding: utf-8 -*-

# IMPORTS
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
import re
import modules.globals as sg

# CLASS DEFINITION
class AssocTrollsCapas(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'assoc_trolls_capas'
    troll_id = Column(Integer, ForeignKey('trolls.user_id', ondelete="CASCADE"), primary_key=True)
    metacapa_id = Column(Integer, ForeignKey('metacapas.id', ondelete="CASCADE"), primary_key=True)
    # ID du groupe d'appartenance
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"), primary_key=True)
    # Niveau
    niv = Column(Integer, default=1, primary_key=True)
    # Pourcentage
    percent = Column(Integer)
    # Subtype
    subtype = Column(String(50))
    # Bonus
    bonus = Column(Integer, default=0)
    
    @hybrid_property
    def nom(self):
        if self.metacapa and self.metacapa.nom:
            return self.metacapa.nom
        return ''
    
    @hybrid_property
    def type(self):
        if self.metacapa and self.metacapa.type:
            return self.metacapa.type
        return ''

    troll = relationship("TROLL", back_populates="capas")
    metacapa = relationship("METACAPA", back_populates="trolls")
    group = relationship('GROUP')

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
        # Return the final formated representation
        res = self.s_long
        res = res.format(o=self)
        res = re.sub(r'None', '', res)
        res = re.sub(r' +', ' ', res)
        return res

