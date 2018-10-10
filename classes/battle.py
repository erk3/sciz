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
    
    # Utility name setter
    def setName(self, prefix, oid, name):
        if len(oid) >= 7 or (len(oid) == 6 and int(oid) > 300000): # Mob
            res = re.search('(((?P<mob_det>une?)\s+)?(?P<mob_name>.+)\s+\[(?P<mob_age>.+)\]\s*(?P<mob_tag>.+)?)(?s)', name)
            setattr(self, prefix + 'mob_nom', res.groupdict()['mob_name'].replace('\r', '').replace('\n', ''))
            setattr(self, prefix + 'mob_age', res.groupdict()['mob_age'].replace('\r', '').replace('\n', ''))
            mob_tag = res.groupdict()['mob_tag']
            if mob_tag:
                setattr(self, prefix + 'mob_tag', mob_tag.replace('\r', '').replace('\n', ''))
            else:
                setattr(self, prefix + 'mob_tag', '')
            setattr(self, prefix + 'mob_id', oid)
        else:
            setattr(self, prefix + 'troll_nom', name.replace('\r', '').replace('\n', ''))
            setattr(self, prefix + 'troll_id', oid)
 
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
        if hasattr(self, 'dead_mult'):
            self.dead = (self.dead or (self.dead_mult is not None)) if hasattr(self, 'dead') else (self.dead_mult is not None)
        if self.subtype is not None:
            self.subtype = self.subtype.strip().capitalize()
            self.subtype += u' esquivé(e)' if self.dodge and not self.parade else ''
            self.subtype += u' parfaitement' if self.perfect_dodge else ''
            self.subtype += u' parée' if self.parade else ''
        else:
            self.subtype = re.sub(u'résistée?|réduit', '', self.type)
        
    def build_att(self):
        # This object is flaged as a duplicate for capa_dead ? Then invert it
        if hasattr(self, 'capa_dead') and self.capa_dead is not None:
            self.alter_capa_dead()
            self.build_def()
            return
        # DEF
        if hasattr(self, 'troll_id') and self.troll_id is not None:
            self.setName('att_', self.troll_id, self.troll_nom)
        elif hasattr(self, 'mob_id') and self.mob_id is not None:
            self.setName('att_', self.mob_id, self.mob_nom)
        # ATT
        if hasattr(self, 'def_id') and self.def_id is not None:
            self.setName('def_', self.def_id, self.def_name)
        if hasattr(self, 'contre_att') and self.contre_att is not None:
            self.subtype = u' Contre-Attaque'
        if hasattr(self, 'resist') and self.resist is not None and not any(i in self.type for i in [u'résisté', u'réduit', u'Insulte', u'Hurlement']):
            self.type += u' résisté'
        self.build()
   
    def build_def(self):
        # DEf
        if hasattr(self, 'troll_id') and self.troll_id is not None:
            self.setName('def_', self.troll_id, self.troll_nom)
        elif hasattr(self, 'mob_id') and self.mob_id is not None:
            self.setName('def_', self.mob_id, self.mob_nom)
        # ATT
        if hasattr(self, 'att_id') and self.att_id is not None:
            self.setName('att_', self.att_id, self.att_name)
        if hasattr(self, 'resist') and self.resist is not None and not any(i in self.type for i in [u'résisté', u'réduit']):
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
    
    def build_def_balayage(self):
        self.build_def()
    
    def build_att_insulte(self):
        if hasattr(self, 'resist') and self.resist is not None:
            self.type += u' sans effet'
        elif hasattr(self, 'insulte_nok') and self.insulte_nok is not None:
            self.type += u' inefficace'
        elif hasattr(self, 'insulte_meh') and self.insulte_meh is not None:
            self.type += u' à l\'effet incertain'
        elif hasattr(self, 'insulte_ok') and self.insulte_ok is not None:
            self.type += u' efficace'
        self.build_att()
    
    def build_att_he(self):
        if hasattr(self, 'resist') and self.resist is not None:
            self.type += u' inefficace'
        else:
            self.type += u' efficace'
        self.build_att()

    def build_att_marquage(self):
        # Tag is already included in the name mob, nothing fancy to do
        self.build_att()

    def alter_capa_dead(self):
        # Zero out everything not needed
        ATTR_TO_KEEP = ['time', 'type', 'group_id', 'troll_id', 'troll_nom', 'def_id', 'def_name']
        ATTRS_TO_DELETE = []
        for attr in vars(self):
            if not attr.startswith('_') and not attr.startswith('capa_dead') and not attr in ATTR_TO_KEEP:
                ATTRS_TO_DELETE.append(attr)
        for attr in ATTRS_TO_DELETE:
            delattr(self, attr)
        # Invert things
        if hasattr(self, 'capa_dead_desc') and self.capa_dead_desc is not None:
            self.type = self.capa_dead_desc
            self.capa_desc = self.capa_dead_desc
        if hasattr(self, 'capa_dead_effet') and self.capa_dead_effet is not None:
            self.capa_effet = self.capa_dead_effet
        if hasattr(self, 'capa_dead_subdesc') and self.capa_dead_subdesc is not None:
            if not hasattr(self, 'capa_dead_effet') or self.capa_dead_effet is None:
                self.capa_effet = self.capa_dead_subdesc
            else:
                self.type += ' (' + self.capa_dead_subdesc + ')'
                self.capa_desc += ' (' + self.capa_dead_subdesc + ')'
        if hasattr(self, 'capa_dead_tour') and self.capa_dead_tour is not None:
            self.capa_tour = self.capa_dead_tour
        if hasattr(self, 'capa_dead_sr') and self.capa_dead_sr is not None:
            self.sr = self.capa_dead_sr
        if hasattr(self, 'capa_dead_resi') and self.capa_dead_resi is not None:
            self.resi = self.capa_dead_resi
        if hasattr(self, 'capa_dead_resist'):
            self.resist = self.capa_dead_resist
        if hasattr(self, 'def_id') and self.def_id is not None:
            self.att_id = self.def_id
            self.att_name = self.def_name

    def stringify(self, reprs, short, attrs):
        # Build the string representations provided
        for (key, value) in reprs:
            s = ''
            try:
                if key.startswith('s_'):
                    setattr(self, key, value)
                    continue
                elif hasattr(self, key) and (getattr(self, key) is not None) and (not isinstance(getattr(self, key), bool) or getattr(self, key)):
                    try:
                        if isinstance(getattr(self, key), (str, unicode)):
                          setattr(self, key, int(getattr(self, key)))
                    except ValueError, TypeError:
                        pass
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
        if self.s_capa_desc and self.s_capa_desc.lower() != self.s_subtype.lower():
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
        res = re.sub(r'\s+', ' ', res)
        res = re.sub(r'\s*%s*\s*$' % self.s_delimiter, '', res)
        res = re.sub(r'\\n', '\n', res)
        return res

    def __getattr__(self, name):
        if hasattr(self, name) or name.startswith('_'):
            return super(BATTLE, self).__getattribute__(name)
        else:
            return None # Trick for the stringify logic (avoiding the raise of an error)
