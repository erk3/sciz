#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import re, datetime, ConfigParser, copy, os
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import modules.globals as sg

# Class of a Battle
class BATTLE(sg.SqlAlchemyBase):
    
    # SQL Table Mapping
    __tablename__ = 'battles'
    __table_args__ = (PrimaryKeyConstraint('id', 'group_id'), )
    # ID unique
    id = Column(Integer, autoincrement=True)
    # Horodatage de l'event
    time = Column(DateTime)
    # ID du troll attaquant
    att_troll_id = Column(Integer, ForeignKey('trolls.id', ondelete="CASCADE"))
    # ID du troll défenseur
    def_troll_id = Column(Integer, ForeignKey('trolls.id', ondelete="CASCADE"))
    # ID du monstre attaquant
    att_mob_id = Column(Integer, ForeignKey('mobs.id', ondelete="CASCADE"))
    # ID du monstre défenseur
    def_mob_id = Column(Integer, ForeignKey('mobs.id', ondelete="CASCADE"))
    # ID du piège
    piege_id = Column(Integer, ForeignKey('pieges.id', ondelete="CASCADE"))
    # ID du groupe
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))
    # Type d'évènement
    type = Column(String(50))
    # Sous type d'évènement
    subtype = Column(String(50))
    # Jet d'attaque
    att = Column(Integer)
    # Jet d'esquive
    esq = Column(Integer)
    # Jet de parade
    par = Column(Integer)
    # Jet de dégâts (sans compter armure)
    deg = Column(Integer)
    # Armure
    arm = Column(Integer)
    # Points de vie perdu par la cible (avec armure)
    pv = Column(Integer)
    # Points de vie restants de la cible
    vie = Column(Integer)
    # Points de vie rendu à la cible
    soin = Column(Integer)
    # Blessure infligée à l'attaquant
    blessure = Column(Integer)
    # Seuil de résistance en %
    sr = Column(Integer)
    # Jet de résistance en %
    resi = Column(Integer)
    # Descritpion de la capacité spéciale
    capa_desc = Column(String(150))
    # Effet de la capacité spéciale
    capa_effet = Column(String(150))
    # Nombre de tours d'effet de la capacité spéciale
    capa_tour = Column(Integer)
    # Evènement résisté ?
    resist = Column(Boolean)
    # Critique ?
    crit = Column(Boolean)
    # Dodge ?
    dodge = Column(Boolean)
    # Perfect dodge ?
    perfect_dodge = Column(Boolean)
    # Parade ?
    parade = Column(Boolean)
    # Cible décédée ?
    dead = Column(Boolean)
    # Gain de RM
    rm = Column(Integer)
    # Gain de MM
    mm = Column(Integer)
    # Gain de PX
    px = Column(Integer)
    # Fatigue
    fatigue = Column(Integer)
    # Direction de la retraite effectuée ?
    retraite = Column(String(50))
    # Jet de déstabilisation
    destab = Column(Integer)
    # Jet de stabilité
    stab = Column(Integer)

    # Associations One-To-Many
    att_troll = relationship("TROLL", primaryjoin="and_(BATTLE.att_troll_id==TROLL.id, BATTLE.group_id==TROLL.group_id)", back_populates="atts")
    def_troll = relationship("TROLL", primaryjoin="and_(BATTLE.def_troll_id==TROLL.id, BATTLE.group_id==TROLL.group_id)", back_populates="defs")
    att_mob = relationship("MOB", primaryjoin="and_(BATTLE.att_mob_id==MOB.id, BATTLE.group_id==MOB.group_id)", back_populates="atts")
    def_mob = relationship("MOB", primaryjoin="and_(BATTLE.def_mob_id==MOB.id, BATTLE.group_id==MOB.group_id)", back_populates="defs")
    piege = relationship("PIEGE", primaryjoin="and_(BATTLE.piege_id==PIEGE.id, BATTLE.group_id==PIEGE.group_id)", back_populates="battles")
    group = relationship("GROUP", back_populates="battles")
    # Associations One-To-One
    event = relationship("EVENT", primaryjoin="and_(BATTLE.id==EVENT.battle_id, BATTLE.group_id==EVENT.group_id)", back_populates="battle", uselist=False)

    # Constructor is handled by SqlAlchemy do not override
    
    # Additional build logics (see MailParser)
    def build(self):
        self.type = self.type.strip().capitalize()
        self.arm = int(self.deg) - int(self.pv) if self.pv and self.deg else None
        self.pv = self.pv or self.deg # Pas d'armure
        self.time = datetime.datetime.strptime(self.time, '%d/%m/%Y  %H:%M:%S')
        if hasattr(self, 'resist'):
            self.resist = self.resist is not None
        if hasattr(self, 'att') and self.att is not None and hasattr(self, 'esq') and self.esq is not None:
            self.crit = int(self.att) > int(self.esq) * 2
            self.dodge = int(self.esq) >= int(self.att)
            self.perfect_dodge = int(self.esq) > int(self.att) * 2
            if hasattr(self, 'par') and self.par is not None:
                self.parade = int(self.par) > (int(self.att) - int(self.esq))
        if hasattr(self, 'destab') and self.destab is not None and hasattr(self, 'stab') and self.stab is not None:
            self.crit = int(self.destab) > int(self.stab) * 2
            self.dodge = int(self.destab) >= int(self.stab)
            self.perfect_dodge = int(self.stab) > int(self.destab) * 2
        if hasattr(self, 'dead'):
            self.dead = self.dead is not None 
        self.dead |= u'mort' in self.type
        if self.subtype is not None:
            self.subtype = self.subtype.strip().capitalize()
            self.subtype += u' esquivé(e)' if self.dodge and not self.parade else ''
            self.subtype += u' parfaitement' if self.perfect_dodge else ''
            self.subtype += u' parée' if self.parade else ''
        else:
            self.subtype = re.sub(u'résistée?|réduit', '', self.type)
        
    def build_att(self):
        # Common
        self.att_troll_id = self.troll_id
        self.att_troll_nom = self.troll_nom
        # ATT
        if hasattr(self, 'def_id') and self.def_id is not None:
            if len(self.def_id) >= 7: # Mob
                res = re.search('(((?P<mob_det>une?)\s+)?(?P<mob_name>.+)\s+\[(?P<mob_age>.+)\]\s*(?P<mob_tag>.+)?)(?s)', self.def_name)
                self.def_mob_nom = res.groupdict()['mob_name'].replace('\r', '').replace('\n', '')
                self.def_mob_age = res.groupdict()['mob_age'].replace('\r', '').replace('\n', '')
                self.def_mob_tag = res.groupdict()['mob_tag']
                if self.def_mob_tag:
                    self.def_mob_tag = self.def_mob_tag.replace('\r', '').replace('\n', '')
                self.def_mob_id = self.def_id
            else:
                self.def_troll_nom = self.def_name
                self.def_troll_id = self.def_id
        if hasattr(self, 'contre_att') and self.contre_att is not None:
            self.subtype = u' Contre-Attaque'
        if hasattr(self, 'resist') and self.resist is not None and not u'résisté' in self.type and not u'réduit' in self.type:
            self.type += u' résisté'
        self.build()
   
    def build_def(self):
        # Common
        self.def_troll_id = self.troll_id
        self.def_troll_nom = self.troll_nom
        # DEF
        if hasattr(self, 'att_id') and self.att_id is not None:
            if len(self.att_id) >= 7: # Mob
                res = re.search('(((?P<mob_det>une?)\s+)?(?P<mob_name>.+)\s+\[(?P<mob_age>.+)\]\s*(?P<mob_tag>.+)?)(?s)', self.att_name)
                self.att_mob_nom = res.groupdict()['mob_name'].replace('\r', '').replace('\n', '')
                self.att_mob_age = res.groupdict()['mob_age'].replace('\r', '').replace('\n', '')
                self.att_mob_tag = res.groupdict()['mob_tag']
                if self.att_mob_tag:
                    self.att_mob_tag = self.att_mob_tag.replace('\r', '').replace('\n', '')
                self.att_mob_id = self.att_id
            else:
                self.att_troll_nom = self.att_name
                self.att_troll_id = self.att_id
        if hasattr(self, 'resist') and self.resist is not None and not u'résisté' in self.type and not u'réduit' in self.type:
            self.type += u' réduit'
        if hasattr(self, 'capa_effet') and self.capa_effet is not None:
            self.capa_effet = re.sub(r'\|$', ' ', self.capa_effet)
            self.subtype = self.capa_desc if self.subtype is None else self.subtype
        if hasattr(self, 'retraite') and self.retraite is not None:
            self.retraite = 'N+' if u"haut" in self.retraite.lower() else self.retraite
            self.retraite = 'N-' if u"bas" in self.retraite.lower() else self.retraite
            self.retraite = 'Y+' if u"nohrdikan" in self.retraite.lower() else self.retraite
            self.retraite = 'Y-' if u"mydikan" in self.retraite.lower() else self.retraite
            self.retraite = 'X+' if u"orhykan" in self.retraite.lower() else self.retraite
            self.retraite = 'X-' if u"oxhykan" in self.retraite.lower() else self.retraite
        self.build()
 
    def build_capa(self):       
        self.build_def()
    
    def build_capa2(self):       
        self.subtype = 'Ronflements' if self.subtype == 'ronfle' else self.subtype
        self.build_capa()
    
    def build_att_sort(self):
        if self.subtype and 'bulle' in self.subtype.lower():
            self.capa_effet = re.sub(ur'sera\s+égale\s+à\s+', '', self.capa_effet);
        self.build_att()
        
    def build_def_sort(self):
        self.build_def()
    
    def build_def_piege(self):
        self.build_def()
    
    def build_att_piege(self):
        self.build_att()
    
    def build_def_parcho(self):
        self.build_def()
    
    def build_def_potion(self):
        self.build_def()
    
    def build_att_ldp(self):
        if self.subtype is None: # potion
            self.type += u' raté'
        self.build_att()
    
    def build_def_ldp(self):
        self.build_def()
    
    def build_att_balayage(self):
        self.build_att()

    def stringify(self, reprs, short, attrs):
        # Build the string representations provided
        for (key, value) in reprs:
            s = ''
            try:
                if key.startswith('s_'):
                    setattr(self, key, value)
                    continue
                elif hasattr(self, key) and (getattr(self, key) is not None) and (not isinstance(getattr(self, key), bool) or getattr(self, key)):
                    s = re.sub(r'\n', ' ', value.format(getattr(self, key)))
            except KeyError as e:
                pass
            setattr(self, 's_' + key, s)
        # Add the time
        self.s_time = sg.format_time(self.time, self.s_time)
        # Add the att an def troll/mob names
        if self.att_troll:
            self.s_att_nom = self.att_troll.stringify_name(self.s_nom_troll)
        elif self.att_mob:
            self.s_att_nom = self.att_mob.stringify_name(self.s_nom_mob)
        else:
            self.s_det_att = ''
            self.s_att_nom = ''
        if self.def_troll:
            self.s_def_nom = self.def_troll.stringify_name(self.s_nom_troll)
        elif self.def_mob:
            self.s_def_nom = self.def_mob.stringify_name(self.s_nom_mob)
        else:
            self.s_det_def = ''
            self.s_def_nom = ''
        # Add the capa
        self.s_capa = self.s_capa_effet
        if self.s_capa_tour:
            self.s_capa = '%s %s' % (self.s_capa, self.s_capa_tour)
        if self.s_capa_desc:
            self.s_capa = '%s %s %s' % (self.s_capa_desc, self.s_delimiter, self.s_capa)
        # Enclose some things
        if self.soin and self.blessure is None and self.pv is not None: # Not sacrifice 
            self.s_soin = '%s%s%s' % (self.s_before, self.s_soin, self.s_after)
        if self.capa_effet and self.pv is not None: # Pouvoir
            self.s_capa = '%s%s%s' % (self.s_before, self.s_capa, self.s_after)
        # Return the final formated representation
        if short: 
            res = self.s_short
        else:
            res = self.s_long
        res = res.format(o=self)
        res = re.sub(r'None', '', res)
        res = re.sub(r'(\(\s*)+', '(', res)
        res = re.sub(r'(\s*\))+', ')', res)
        res = re.sub(r'(\)\()|(\(\))', ' ', res)
        res = re.sub(r'\s*:(\s*|\n|\\n)*(\(|$)', r' \2', res)
        res = re.sub(r' +', ' ', res)
        res = re.sub(r'\\n', '\n', res)
        return res

    def __getattr__(self, name):
        if hasattr(self, name) or name.startswith('_'):
            return super(BATTLE, self).__getattribute__(name)
        else:
            return None # Trick for the stringify logic (avoiding the raise of an error)
