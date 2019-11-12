#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.being_troll_private import TrollPrivate
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import modules.globals as sg
import re, math


# CLASS DEFINITION
class TrollPrivateCapa(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Public Troll ID
    troll_id = Column(Integer, ForeignKey('being_troll.id', ondelete='CASCADE'))
    # Troll who has a view on the privates capas of this troll
    viewer_id = Column(Integer, ForeignKey('being_troll.id', ondelete='CASCADE'))
    # MetaCapa ID
    metacapa_id = Column(Integer, ForeignKey('capa_meta.id', ondelete="CASCADE"))
    # Level
    niv = Column(Integer, default=1)
    # Pourcentage
    percent = Column(Integer)
    # Subtype
    subtype = Column(String(50))
    # Bonus
    bonus = Column(Integer, default=0)

    # Associations
    troll = relationship('Troll', back_populates='troll_privates_capas', primaryjoin='TrollPrivateCapa.troll_id == Troll.id')
    viewer = relationship('Troll', back_populates='viewed_troll_privates_capas', primaryjoin='TrollPrivateCapa.viewer_id == Troll.id')
    troll_private = relationship('TrollPrivate', back_populates='troll_privates_capas', primaryjoin='and_(foreign(TrollPrivateCapa.troll_id) == TrollPrivate.troll_id, foreign(TrollPrivateCapa.viewer_id) == TrollPrivate.viewer_id)', remote_side=(TrollPrivate.troll_id, TrollPrivate.viewer_id))
    metacapa = relationship('MetaCapa', primaryjoin='TrollPrivateCapa.metacapa_id == MetaCapa.id')

    # SQL Table Mapping
    __tablename__ = 'being_troll_private_capa'
    __table_args__ = (PrimaryKeyConstraint('troll_id', 'viewer_id', 'metacapa_id', 'niv'), )

    @hybrid_property
    def nom(self):
        if self.metacapa is not None and self.metacapa.nom is not None:
            return self.metacapa.nom
        return None

    @hybrid_property
    def type(self):
        if self.metacapa is not None and self.metacapa.type is not None:
            return self.metacapa.type
        return None

    @hybrid_property
    def values(self):
        if sg.formulas is not None and self.metacapa is not None and self.metacapa.nom is not None and self.troll_private is not None:
            res = ''
            if self.metacapa.nom in sg.formulas:
                formula = sg.formulas[self.metacapa.nom]
                for attr in formula:
                    try:
                        _min, _max, _bonus = None, None, None
                        base = formula[attr][sg.CONF_FORMULA_BASE]
                        base = re.sub(r'(?P<attr>bonus_[a-zA-Z_]+)', 'self.troll_private.\g<attr>', base)
                        _min = float(eval('f"{%s}"' % re.sub(r'(?P<attr>base_\w+)', 'self.troll_private.\g<attr>_min', base)))
                        _max = float(eval('f"{%s}"' % re.sub(r'(?P<attr>base_[a-zA-Z]+)', 'self.troll_private.\g<attr>_max', base)))
                        _max = math.ceil(_max) if _min != _max else math.floor(_max)
                        _min = math.floor(_min)
                        bonus = formula[attr][sg.CONF_FORMULA_BONUS]
                        if len(bonus) > 0:
                            bonus = re.sub(r'(?P<attr>bonus_[a-zA-Z_]+)', 'self.troll_private.\g<attr>', bonus)
                            bonus = re.sub(r'(?P<attr>base_[a-zA-Z]+)', 'self.troll_private.\g<attr>_min', bonus)
                            bonus = math.floor(float(eval('f"{%s}"' % bonus)))
                        else:
                            bonus = None
                        # Build result
                        texte = formula[attr][sg.CONF_FORMULA_TEXT]
                        if _min is not None or _max is not None:
                            res += eval('f"%s ; "' % texte)
                    except Exception as e:
                        sg.logger.error('Error in formula "%s" attr "%s"' % (formula, attr))
                        sg.logger.exception(e)
                        continue
                return res[:-3] if len(res) > 3 else res
        return None
