#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import re, datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a AA
class AA(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'aas'
    __table_args__ = (PrimaryKeyConstraint('id', 'group_id'), )
    # ID unique
    id = Column(Integer, autoincrement=True)
    # Horodatage de l'AA
    time = Column(DateTime)
    # ID du troll 
    troll_id = Column(Integer, ForeignKey('trolls.id', ondelete="CASCADE"))
    # ID du troll cible
    troll_cible_id = Column(Integer, ForeignKey('trolls.id', ondelete="CASCADE"))
    # ID du groupe
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    # Pourcentage de blessure du troll
    blessure = Column(Integer)
    # Niveau
    niv = Column(Integer)
    # Points de Vie minimum
    pv_min = Column(Integer)
    # Points de Vie maximum
    pv_max = Column(Integer)
    # Attaque minimum en D6
    att_min = Column(Integer)
    # Attaque maximum en D6
    att_max = Column(Integer)
    # Esquive minimum en D6
    esq_min = Column(Integer)
    # Esquive maximum en D6
    esq_max = Column(Integer)
    # Dégâts minimum en D3
    deg_min = Column(Integer)
    # Dégâts maximum en D3
    deg_max = Column(Integer)
    # Régénération minimum en D3
    reg_min = Column(Integer)
    # Régénération maximum en D3
    reg_max = Column(Integer)
    # Armure physique minimum
    arm_phy_min = Column(Integer)
    # Armure physique maximum
    arm_phy_max = Column(Integer)
    # Vue minimum en nombre de cases
    vue_min = Column(Integer)
    # Vue maximum en nombre de cases
    vue_max = Column(Integer)
    
    # Associations One-To-Many
    troll = relationship("TROLL", primaryjoin="and_(AA.troll_id==TROLL.id, AA.group_id==TROLL.group_id)", back_populates="aas")
    troll_cible = relationship("TROLL", primaryjoin="and_(AA.troll_cible_id==TROLL.id, AA.group_id==TROLL.group_id)", back_populates="aas")
    group = relationship("GROUP", back_populates="aas")
    # Association One-To-One
    event = relationship("EVENT", primaryjoin="and_(AA.id==EVENT.aa_id, AA.group_id==EVENT.group_id)", back_populates="aa", uselist=False)

    # Constructor is handled by SqlAlchemy do not override
    
    # Additional build logics
    def build(self):
        self.time = datetime.datetime.strptime(self.time, '%d/%m/%Y  %H:%M:%S')
        # AA Niv 1
        self.pv_min = self.pv_min or self.pv_sup or self.pv_eq
        self.pv_max = self.pv_max or self.pv_inf or self.pv_eq
        self.att_min = self.att_min or self.att_sup or self.att_eq
        self.att_max = self.att_max or self.att_inf or self.att_eq
        self.esq_min = self.esq_min or self.esq_sup or self.esq_eq
        self.esq_max = self.esq_max or self.esq_inf or self.esq_eq
        self.deg_min = self.deg_min or self.deg_sup or self.deg_eq
        self.deg_max = self.deg_max or self.deg_inf or self.deg_eq
        self.reg_min = self.reg_min or self.reg_sup or self.reg_eq
        self.reg_max = self.reg_max or self.reg_inf or self.reg_eq
        self.arm_phy_min = self.arm_phy_min or self.arm_phy_sup or self.arm_phy_eq
        self.arm_phy_max = self.arm_phy_max or self.arm_phy_inf or self.arm_phy_eq
        self.vue_min = self.vue_min or self.vue_sup or self.vue_eq
        self.vue_max = self.vue_max or self.vue_inf or self.vue_eq
                    
    def stringify(self, reprs, short, attrs):
        # Build the string representations provided
        for (key, value) in reprs:
            s = ''
            try:
                if key.startswith('s_'):
                    setattr(self, key, value)
                    continue
                elif hasattr(self, key) and getattr(self, key) is not None:
                    try:
                        if isinstance(getattr(self, key), (str, unicode)):
                          setattr(self, key, int(getattr(self, key)))
                    except ValueError, TypeError:
                        pass
                    if isinstance(getattr(self, key), bool):
                        s = value.format(sg.boolean2French(getattr(self, key)))
                    else:
                        s = value.format(getattr(self, key))
                elif hasattr(self, key + '_min') or hasattr(self, key + '_max'):
                    s = sg.str_min_max(getattr(self, key+ '_min'), getattr(self, key + '_max'))
                    s = value.format(s) if s is not None else ''
            except KeyError as e:
                pass
            setattr(self, 's_' + key, s)
        # Add the time
        self.s_time = sg.format_time(self.time, self.s_time)
        # Add the troll names
        self.s_troll_nom = self.troll.stringify_name()
        self.s_troll_cible_nom = self.troll_cible.stringify_name()
        # Return the final formated representation
        if short:
            res = self.s_short
        else:
            res = self.s_long
        self.s_aa_stats = self.s_aa_stats.format(o=self)
        res = res.format(o=self)
        res = res.encode(sg.DEFAULT_CHARSET).decode('string-escape').decode(sg.DEFAULT_CHARSET)
        res = re.sub(r'None', '', res)
        res = re.sub(r'\s*%s+\s*' % self.s_sep, '%s' % (self.s_sep), res)
        res = re.sub(r'%s$' % self.s_sep, '', res)
        res = re.sub(r' +', ' ', res)
        return res

    def __getattr__(self, name):
        if hasattr(self, name) or name.startswith('_'):
            return super(AA, self).__getattribute__(name)
        else:
            return None # Trick for the stringify logic (avoiding the raise of an error)
