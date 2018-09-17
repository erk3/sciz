#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import re, datetime, ConfigParser
import modules.globals as sg

# Class of an Identification Des Trésors
class IDT(sg.SqlAlchemyBase):

    # SQL Table Mapping
    __tablename__ = 'idts'
    __table_args__ = (PrimaryKeyConstraint('id', 'group_id'), )
    # Identifiant unique
    id = Column(Integer, autoincrement=True)
    # ID du trésor
    tresor_id = Column(Integer)#, ForeignKey('tresors.id', ondelete="CASCADE"))
    # ID du méta-trésor
    metatresor_id = Column(Integer, ForeignKey('metatresors.id', ondelete="SET NULL"))
    # Date de création
    time = Column(DateTime())
    # ID du troll
    troll_id = Column(Integer, ForeignKey('trolls.id', ondelete="CASCADE"))
    # ID du groupe d'appartenance
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    # Nom de l'objet
    type = Column(String(250))
    # Templates de l'objet
    templates = Column(String(250))
    # Mithril ?
    mithril = Column(Boolean)
    # Effet de l'objet
    effet = Column(String(250))
    # Pos X du trésor
    posx = Column(Integer)
    # Pos Y du trésor
    posy = Column(Integer)
    # Pos N du trésor
    posn = Column(Integer)

    # Associations One-To-Many
    group = relationship("GROUP", back_populates="idts")
    troll = relationship("TROLL", primaryjoin="and_(IDT.troll_id==TROLL.id, IDT.group_id==TROLL.group_id)", back_populates="idts")
    metatresor = relationship("METATRESOR", back_populates="idts")
    # Associations One-To-One
    event = relationship('EVENT', primaryjoin="and_(IDT.id==EVENT.idt_id, IDT.group_id==EVENT.group_id)", back_populates='idt', uselist=False)

    # Constructor is handled by SqlAlchemy, do not override

    # Loop over every metatresors in the list to find the longest one matching the mob name...
    def link_metatresor(self, metatresors):
        result_id = -1
        result_nom = ''
        if self.type is not None:
            for metatresor in metatresors:
                if metatresor.nom in self.type and len(metatresor.nom) > len(result_nom):
                    result_nom = metatresor.nom
                    result_id = metatresor.id
            if result_id > 0:
                self.metatresor_id = result_id
                # Split name and templates
                if len(result_nom) < len(self.type):
                    self.templates = re.sub(result_nom, '', self.type)
                    self.type = result_nom
            else:
                sg.logger.warning('Cannot match \'%s\' to a metatresor' % self.type)
        else:
            sg.logger.error('Tresor has no name, cannot search for a metatresor to link')
    
    # Additional build logic (see MailParser)
    def build(self):
        self.time = datetime.datetime.strptime(self.time, '%d/%m/%Y  %H:%M:%S')
        self.type = re.sub(r'\n', ' ', self.type).strip()
        if self.type == u'Malédiction':
            self.type = 'Mission maudite'
        if self.effet is not None:
            self.effet = re.sub(r'\n', ' ', self.effet).strip()
            if self.effet == '' or self.effet == u'Spécial':
                del self.effet
        if hasattr(self, 'mithril'):
            self.mithril = self.mithril is not None 
        # Special handling for maps
        res = re.search('((?P<nom>Carte des Raccourcis) : (?P<effet>\w+))(?s)', self.type)
        if res is not None:
            self.type = res.groupdict()['nom']
            self.effet = res.groupdict()['effet']

    def stringify(self, reprs, short, attrs):
        # Build the string representations provided
        for (key, value) in reprs:
            s = ''
            try:
                if key.startswith('s_'):
                    setattr(self, key, value)
                    continue
                elif hasattr(self, key) and getattr(self, key) is not None and (not isinstance(getattr(self, key), bool) or getattr(self, key)):
                    try: 
                        setattr(self, key, int(getattr(self, key)))
                    except ValueError:
                        pass
                    s = value.format(getattr(self, key))
            except KeyError as e:
                pass
            setattr(self, 's_' + key, s)
        # Add the time
        self.s_time = sg.format_time(self.time, self.s_time)
        # Add the troll name
        self.s_nom_full = self.troll.stringify_name()
        # Compute some additional things
        self.s_pos = self.s_pos.format(o=self) if self.s_posx != '' else ''
        # Return the final formated representation
        if short:
            res = self.s_short
        else:
            res = self.s_long
        res = res.format(o=self)
        res = re.sub(r'None', '', res)
        res = re.sub(r' +', ' ', res)
        return res

    def __getattr__(self, name):
        if hasattr(self, name) or name.startswith('_'):
            return super(IDT, self).__getattribute__(name)
        else:
            return None # Trick for the stringify logic (avoiding the raise of an error)
