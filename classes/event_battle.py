#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.being import Being
from classes.being_mob import Mob
from classes.being_mob_private import MobPrivate
from classes.being_troll import Troll
from classes.being_troll_private import TrollPrivate
from classes.tresor import Tresor
from classes.tresor_private import TresorPrivate
from classes.event import Event
from classes.lieu_piege import Piege
from sqlalchemy import event, and_, Column, Integer, String, Boolean, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
import re, math, datetime
import modules.globals as sg


# CLASS DEFINITION
class battleEvent(Event):

    # Constructor is handled by SqlAlchemy do not override

    # Unique identifier
    id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    # Attacker ID
    att_id = Column(Integer, ForeignKey('being.id'))
    # Attacker name
    att_nom = Column(String(100))
    # Defender ID
    def_id = Column(Integer, ForeignKey('being.id'))
    # Defender ID
    def_nom = Column(String(100))
    # Interposing being ID
    autre_id = Column(Integer, ForeignKey('being.id'))
    # Interposing being name
    autre_nom = Column(String(100))
    # Place id (for example a trap if trigerred)
    lieu_id = Column(Integer, ForeignKey('lieu.id'))
    # Treasure id (if one used or affected)
    tresor_id = Column(Integer, ForeignKey('tresor.id'))
    # Treasure name (if one used or affected)
    tresor_nom = Column(String(100))
    # Mushroom id (if one used)
    champi_id = Column(Integer, ForeignKey('champi.id'))
    # Event type
    type = Column(String(250))
    # ATT rolled
    att = Column(Integer)
    # ESQ rolled
    esq = Column(Integer)
    # PAR rolled
    par = Column(Integer)
    # REF rolled
    ref = Column(Integer)
    # DEG rolled
    deg = Column(Integer)
    # Destabilization rolled
    destab = Column(Integer)
    # Stabilization rolled
    stab = Column(Integer)
    # Lost life points
    pdv = Column(Integer)
    # Remaining life points of the defender or interposing being
    vie = Column(Integer)
    # Life points healed
    soin = Column(Integer)
    # Life points sacrified
    blessure = Column(Integer)
    # Threshold of resistance
    sr = Column(Integer)
    # Resistance rolled
    resi = Column(Integer)
    # Flag 'resisted' ? (Sometimes no sr/resi, just the flag)
    flag_resist = Column(Boolean)
    # Special ability description
    capa_desc = Column(String(150))
    # Special ability effect
    capa_effet = Column(String(150))
    # Special ability duration (T)
    capa_tour = Column(Integer)
    # X axis position (Trap, tracking, etc.)
    pos_x = Column(Integer)
    # Y axis position (Trap, tracking, etc.)
    pos_y = Column(Integer)
    # N axis position (Trap, tracking, etc.)
    pos_n = Column(Integer)
    # Direction for what?
    dir_for = Column(String(50))
    # X axis direction (Retreat, tracking, etc.)
    dir_x = Column(String(25))
    # Y axis direction (Retreat, tracking, etc.)
    dir_y = Column(String(25))
    # N axis direction (Retreat, tracking, etc.)
    dir_n = Column(String(25))

    @hybrid_property
    def pv(self):
        if self.pdv is not None:
            return self.pdv
        return self.deg

    @hybrid_property
    def str_vie(self):
        return None if self.vie is None or int(self.vie) < 1 else self.vie
        return arm

    @hybrid_property
    def arm(self):
        arm = None
        if all(attr is not None for attr in [self.deg, self.pv]):
            arm = int(self.deg) - int(self.pv)
        arm = None if arm is None or arm < 1 else arm
        return arm

    @hybrid_property
    def esquive_parfaite(self):
        if all(attr is not None for attr in [self.att, self.esq]):
            return int(self.esq) >= int(self.att) * 2
        elif all(attr is not None for attr in [self.destab, self.stab]):
            return int(self.stab) >= int(self.destab) * 2
        return False

    @hybrid_property
    def parade(self):
        if all(attr is not None for attr in [self.par, self.att, self.esq]):
            return int(self.esq) + int(self.par) >= int(self.att)
        return False

    @hybrid_property
    def esquive(self):
        if all(attr is not None for attr in [self.att, self.esq]):
            return int(self.esq) >= int(self.att)
        elif all(attr is not None for attr in [self.destab, self.stab]):
            return int(self.stab) >= int(self.destab)
        return False

    @hybrid_property
    def critique(self):
        if all(attr is not None for attr in [self.att, self.esq]):
            return int(self.att) > int(self.esq) * 2
        elif all(attr is not None for attr in [self.att, self.ref]):
            return int(self.att) > int(self.ref)
        elif all(attr is not None for attr in [self.destab, self.stab]):
            return int(self.destab) > int(self.stab) * 2
        return False

    @hybrid_property
    def resist(self):
        if self.flag_resist:
            return True
        elif all(attr is not None for attr in [self.sr, self.resi]):
            return int(self.resi) <= int(self.sr)
        return False

    @hybrid_property
    def mort(self):
        return self.vie is not None and int(self.vie) <= 0

    @hybrid_property
    def tresor_private(self):
        return sg.db.session.query(TresorPrivate).get((self.tresor_id, self.owner_id))

    @hybrid_property
    def subtype(self):
        subtype = ''
        subtype += ' critique' if self.critique else ''
        subtype += ' résisté(e)' if self.resist else ''
        subtype += ' esquivé(e)' if self.esquive else ''
        subtype += ' parfaitement' if self.esquive_parfaite else ''
        subtype += ' paré(e)' if self.parade else ''
        return subtype.strip()

    # Associations
    att_being = relationship('Being', primaryjoin='battleEvent.att_id == Being.id')
    def_being = relationship('Being', primaryjoin='battleEvent.def_id == Being.id')
    autre_being = relationship('Being', primaryjoin='battleEvent.autre_id == Being.id')
    lieu = relationship('Lieu', primaryjoin='battleEvent.lieu_id == Lieu.id')
    tresor = relationship('Tresor', primaryjoin='battleEvent.tresor_id == Tresor.id')
    champi = relationship('Champi', primaryjoin='battleEvent.champi_id == Champi.id')

    # SQL Table Mapping
    __tablename__ = 'event_battle'
    __mapper_args__ = {
        'polymorphic_identity': 'Combat',
        'inherit_condition': id == Event.id
    }

    # Additional build logics
    def build(self):
        super().build()
        # Fix att/def_being
        fix_id = self.suivant_id if hasattr(self, 'suivant_id') else self.owner_id
        fix_nom = self.suivant_nom if hasattr(self, 'suivant_nom') else self.owner_nom
        if self.att_id is None and self.def_id is None:
            if hasattr(self, 'flag_def') and self.flag_def is not None:
                self.def_id, self.def_nom = fix_id, fix_nom
            else:
                self.att_id, self.att_nom = fix_id, fix_nom
        elif self.att_id is not None and self.def_id is None and (self.att_id != fix_id or hasattr(self, 'flag_ldp')):
            self.def_id, self.def_nom = fix_id, fix_nom
        elif self.att_id is None and self.def_id is not None and (self.def_id != fix_id or hasattr(self, 'flag_ldp')):
            self.att_id, self.att_nom = fix_id, fix_nom
        if self.autre_id is not None and self.type is not None and 'interposition' in self.type.lower():
            self.type = 'Attaque'
        # If the event is a duplicata for capabilities of monsters triggered at death, reverse it instead of doing the following
        if hasattr(self, 'capa_dead') and self.capa_dead is not None:
            self.build_reverse()
            return
        # Fix BAM/BUM
        if self.type is not None and 'bulle' in self.type.lower():
            self.capa_effet = ' ' + re.sub(r'sera\s+égale\s+à\s+', '', self.capa_effet)
            if hasattr(self, 'capa_desc') and self.capa_desc is not None:
                self.capa_desc = 'Portail ' + ('d\'arrivée ' if 'arrivant' in self.capa_desc else 'de départ ') + self.capa_desc.split(' ')[0]
        # Fix Baroufle
        if self.type is not None and 'baroufle' in self.type.lower():
            if 'concentration' in self.capa_effet.lower() and self.capa_effet.count('\n-') == 0:
                self.capa_tour = None
            for r,v in [(r'(E|e)ffet\s+(I|i)mm(é|e)diat\s*\:(.*?)(;|\n|$)', r'\4'),
                        (r'-.*?quelque\s+chose\s+de\s+magique.*?(;|\n|$)', ''),
                        (r'-.*?(donne\s+envie\s+de\s+danser|Vous\s+dansez).*?(;|\n|$)', ''),
                        (r'(\:\s*de)', '')]:
                self.capa_effet = re.sub(r, v, self.capa_effet)
            self.capa_effet = re.sub(r'-', '', self.capa_effet, count=1)
            self.capa_effet = re.sub(r'\n\s*-', ' ;', self.capa_effet)
            if hasattr(self, 'flag_baroufle_portee') and self.flag_baroufle_portee is not None:
                self.capa_effet += ('' if self.capa_effet == '' else ' ;') + ' Portée +1'
            if hasattr(self, 'flag_baroufle_sssrileur') and self.flag_baroufle_sssrileur is not None:
                self.capa_effet += ('' if self.capa_effet == '' else ' ;') + ' Rend visible'
            if hasattr(self, 'flag_baroufle_ytseukayndof') and self.flag_baroufle_ytseukayndof is not None:
                self.capa_effet += ('' if self.capa_effet == '' else ' ;') + ' BM magiques'
            if hasattr(self, 'flag_baroufle_ghimighimighimi') and self.flag_baroufle_ghimighimighimi is not None:
                self.capa_effet += ('' if self.capa_effet == '' else ' ;') + ' Autobaroufle'
        # Fix Camouflage effect for PM
        if self.type is not None and 'projectile' in self.type.lower() and self.capa_effet is not None and 'camouflage' in self.capa_effet.lower():
            self.capa_effet = re.sub(r'(est|a\s+été)\s+', '', self.capa_effet.capitalize())
        # Fix snoring of monsters
        if self.type == 'ronfle':
            self.type = 'Ronflements'
        # Fix treasure eating
        if self.type == 'mangé':
            self.type = 'Machouillage'
        # Fix ejection
        if self.type == 'a éjecté':
            self.type = 'Ejection'
        # Fix smoking by monsters
        if self.type == 'enfumé':
            self.type = 'Enfumage'
        # Fix attraction from monsters
        if self.type == 'a attiré' or self.type == 'assomme':
            self.type = 'Attraction assommante'
        # Fix HE & Insulte
        if hasattr(self, 'flag_he_insulte') and self.flag_he_insulte is not None:
            if hasattr(self, 'flag_insulte_nok') and self.flag_insulte_nok is not None:
                self.type += ' inefficace'
            elif hasattr(self, 'flag_insulte_meh') and self.flag_insulte_meh is not None:
                self.type += ' à l\'effet incertain'
            elif not hasattr(self, 'flag_resist') or self.flag_resist is None:
                self.type += ' efficace'
        # Fix CA
        if hasattr(self, 'ca') and self.ca is not None:
            self.type = 'Contre-Attaque'
        # Fix Charge
        if self.type is not None and 'Charger' in self.type:
            self.type = self.type.replace('Charger', 'Charge')
        # Fix planned Parade if necessary
        if self.type is not None and 'Parer' in self.type:
            self.type = self.type.replace('Parer', 'Parade')
        # Fix Mouchoo
        if self.type is not None and 'mouches' in self.type:
            self.type = self.type.replace('mouches', 'Vol de mouches')
        # Fix tracking and retreat
        if hasattr(self, 'direction') and self.direction is not None:
            if 'orhykan' in self.direction.lower(): self.dir_x = 'X+'
            if 'oxhykan' in self.direction.lower(): self.dir_x = 'X-'
            if 'nohrdikan' in self.direction.lower(): self.dir_y = 'Y+'
            if 'mydikan' in self.direction.lower(): self.dir_y = 'Y-'
            if 'haut' in self.direction.lower(): self.dir_n = 'N+'
            if 'bas' in self.direction.lower(): self.dir_n = 'N-'
        if hasattr(self, 'flag_pistage_hors') and self.flag_pistage_hors is not None:
            self.dir_x = 'hors de portée'
        if hasattr(self, 'flag_pistage_zone') and self.flag_pistage_zone is not None:
            self.dir_x = 'sur zone'
        # Fix capa
        if hasattr(self, 'capa_effet') and self.capa_effet is not None:
            self.capa_effet = re.sub(r'\|$', ' ', self.capa_effet).strip()
            if self.type is not None and 'métabolisme' in self.type:
                self.capa_effet = '-' + self.capa_effet
                if hasattr(self, 'dla') and self.dla is not None:
                    self.capa_effet += '; DLA ' + self.dla
        if hasattr(self, 'capa_desc') and self.capa_desc is not None:
            self.capa_desc = re.sub('\s+', ' ', self.capa_desc).strip().capitalize()
            # Fix EA
            if 'aléatoire' in self.capa_desc:
                self.capa_effet = self.capa_effet.capitalize()
        # Ultimate attempt to have a type
        if self.type is None and hasattr(self, 'capa_desc') and self.capa_desc is not None:
            self.type = self.capa_desc
        if self.type is not None and self.capa_desc is not None:
            if self.type.strip().capitalize() != self.capa_desc.strip().capitalize() and self.type.startswith('Attaque'):
                self.type = re.sub('Attaque', self.capa_desc, self.type)
                self.capa_desc = None
            elif self.type.strip().capitalize() == self.capa_desc.strip().capitalize():
                self.capa_desc = None
        # Add suffix for planned actions
        if hasattr(self, 'prog') and self.prog is not None:
            self.type += ' ' + self.prog
        # Fix the type
        self.type = self.type.replace('\r', '').replace('\n', ' ').strip().capitalize()
        self.type = re.sub(r'critique|résistée?|mortelle|esquivée?|parfaitement', '', self.type)
        # Fix LDP
        if hasattr(self, 'flag_ldp') and self.flag_ldp is not None:
            if hasattr(self, 'type_potion') and self.type_potion is not None:
                self.type = self.type.replace('potion', self.type_potion)
        if hasattr(self, 'flag_ldp_rate') and self.flag_ldp_rate is not None:
            self.type += ' raté'
        # Handle the flags
        if hasattr(self, 'flag_resist_att_mag'):
            self.flag_resist = self.flag_resist_att_mag is not None and (not hasattr(self, 'capa_effet') or self.capa_effet is None)
        if hasattr(self, 'flag_resist'):
            self.flag_resist = self.flag_resist is not None and self.flag_resist != False
        if hasattr(self, 'flag_dead') and self.flag_dead is not None: self.vie = 0
        if hasattr(self, 'flag_dead_mult') and self.flag_dead_mult is not None: self.vie = 0

    def build_reverse(self):
        # Zero out everything not needed
        ATTR_TO_KEEP = ['time', 'type', 'owner_id', 'owner_nom', 'att_id', 'att_nom', 'def_id', 'def_nom', 'mh_type', 'sciz_type', 'mail_subject', 'mail_body']
        ATTRS_TO_DELETE = []
        for attr in vars(self):
            if not attr.startswith('_') and not attr.startswith('capa_dead') and attr not in ATTR_TO_KEEP:
                ATTRS_TO_DELETE.append(attr)
        for attr in ATTRS_TO_DELETE:
            delattr(self, attr)
        # Invert things
        tmp_id, tmp_nom = self.att_id, self.att_nom
        self.att_id, self.att_nom = self.def_id, self.def_nom
        self.def_id, self.def_nom = tmp_id, tmp_nom
        if hasattr(self, 'capa_dead_desc') and self.capa_dead_desc is not None:
            self.type = re.sub('\s+', ' ', self.capa_dead_desc).strip()
            self.type = re.sub('la Bénédiction', 'Bénédiction', self.type) # Delete the prefix for Coccicruelle
            if 'substance visqueuse et corrosive' in self.type: # Delete the prefix for Essaim
                self.type = 'Explosion visqueuse et corrosive'
        if hasattr(self, 'capa_dead_effet') and self.capa_dead_effet is not None:
            self.capa_effet = re.sub('\s+', ' ', self.capa_dead_effet).strip().capitalize()
        if hasattr(self, 'capa_dead_subdesc') and self.capa_dead_subdesc is not None:
            self.capa_dead_subdesc = re.sub('\s+', ' ', self.capa_dead_subdesc).strip().capitalize()
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
            self.flag_resist = self.capa_dead_resist is not None


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(battleEvent, 'before_insert')
def upsert_targetted_beings(mapper, connection, target):
    # Beings
    objs = []
    if target.att_id is not None:
        target.att_nom = re.sub('\s+', ' ', target.att_nom).strip()
        objs.append({'id': target.att_id, 'nom': target.att_nom, 'mort': False})
    if target.def_id is not None:
        target.def_nom = re.sub('\s+', ' ', target.def_nom).strip()
        objs.append({'id': target.def_id, 'nom': target.def_nom, 'mort': (target.vie is not None and int(target.vie) <= 0)})
    if target.autre_id is not None:
        target.autre_nom = re.sub('\s+', ' ', target.autre_nom).strip()
        objs.append({'id': target.autre_id, 'nom': target.autre_nom, 'mort': False})
    for obj in objs:
        if Being.is_mob(obj['id']):
            sg.db.upsert(Mob(id=obj['id'], nom=obj['nom'], mort=obj['mort']))
        else:
            sg.db.upsert(Troll(id=obj['id'], nom=obj['nom']))
    # Treasure
    if target.tresor_id is not None:
        if target.tresor_nom is not None:
            target.tresor_nom = re.sub('\s+', ' ', target.tresor_nom).strip()
        tresor = sg.db.session.query(Tresor).get(target.tresor_id)
        if tresor is None:
            tresor = Tresor(id=target.tresor_id)
            sg.db.upsert(tresor)


@event.listens_for(battleEvent, 'before_insert')
def mark_old_piege_destroyed_and_link(mapper, connection, target):
    try:
        piege = sg.db.session.query(Piege).filter(and_(Piege.owner_id != target.owner_id,
                                                       Piege.pos_x == target.pos_x,
                                                       Piege.pos_y == target.pos_y,
                                                       Piege.pos_n == target.pos_n)).one()
        target.lieu_id = piege.id
        piege.destroyed = True
        sg.db.upsert(piege)
    except (NoResultFound, MultipleResultsFound):
        pass


@event.listens_for(battleEvent, 'before_insert')
def upsert_privates(mapper, connection, target):
    # Beings
    beings = [target.att_id, target.def_id, target.autre_id]
    beings = list(filter(lambda x : x is not None, beings))
    for being in beings:
        if Mob.is_mob(being):
            mob_private = sg.db.session.query(MobPrivate).get((being, target.owner_id))
            if mob_private is None: mob_private = MobPrivate(mob_id=being, viewer_id=target.owner_id)
            mob_private.last_event_update_at = target.time
            mob_private.last_event_update_by = target.owner_id
            sg.db.upsert(mob_private)
        else:
            troll_private = sg.db.session.query(TrollPrivate).get((being, target.owner_id))
            if troll_private is None: troll_private = TrollPrivate(troll_id=being, viewer_id=target.owner_id)
            troll_private.last_event_update_at = target.time
            troll_private.last_event_update_by = target.owner_id
            sg.db.upsert(troll_private)
    # Treasure
    if target.tresor_id is not None:
        tresor_private = sg.db.session.query(TresorPrivate).get((target.tresor_id, target.owner_id))
        if tresor_private is None and target.tresor_nom is not None:
            tresor_private = TresorPrivate(tresor_id=target.tresor_id, viewer_id=target.owner_id)
            tresor_private.nom = target.tresor_nom
            sg.db.upsert(tresor_private)


@event.listens_for(battleEvent, 'before_insert')
def play(mapper, connection, target):
    t = target.type.lower()
    # Attacker is a troll
    if target.att_id is not None and not Being.is_mob(target.att_id):
        at = sg.db.session.query(TrollPrivate).get((target.att_id, target.owner_id))
        if target.blessure is not None and at.pdv is not None and int(target.blessure) > 0:
            at.pdv = max(0, at.pdv - int(target.blessure))
        if target.fatigue is not None and int(target.fatigue) > 0:
            fatigue = at.fatigue if at.fatigue is not None else 0
            at.fatigue = max(127, fatigue + int(target.fatigue))
        if target.mm is not None and int(target.mm) > 0:
            at.base_mm_min = (at.base_mm_min if at.base_mm_min is not None else 0) + int(target.mm)
            at.base_mm_max = (at.base_mm_max if at.base_mm_max is not None else 0) + int(target.mm)
        at.invisibilite = 'invisibilité' in t
        at.camouflage = 'camouflage' in t
        at.levitation = 'levitation' in t
        if 'retraite programmée' in t:
            at.nb_retraite_prog = 1
        if 'contre-attaque programmée' in t:
            at.nb_ctr_att_prog = 1
        if 'parade programmée' in t:
            at.nb_parade_prog = 1
        # Update the event
        if 'hypnotisme' in t and at.base_esq_min is not None:
            dim = math.trunc(at.base_esq_min * 1.5) if not target.resist else math.trunc(at.base_esq_min / 3)
            target.capa_effet = f'ESQ -{dim}D6'
        if 'siphon' in t and target.capa_effet is not None:
            target.capa_effet = f'ATT -{target.capa_effet}'
            target.capa_tour = 1 if target.resist else 2
        if 'rafale' in t and target.capa_effet is not None:
            target.capa_effet = f'REG -{target.capa_effet}'
            target.capa_tour = 1 if target.resist else 2
        if 'métabolisme' in t:
            match = re.search('DLA (.+)', target.capa_effet)
            if match is not None:
                at.next_dla = datetime.datetime.strptime(match.group(1), '%d/%m/%Y  %H:%M:%S')
        sg.db.upsert(at)
    # Defenser is a troll
    if target.def_id is not None and not Being.is_mob(target.def_id):
        dt = sg.db.session.query(TrollPrivate).get((target.def_id, target.owner_id))
        if target.soin is not None and dt.pdv is not None and dt.base_pdv_max is not None and int(target.soin) > 0:
            dt.pdv = min(dt.pdv + int(target.soin), dt.base_pdv_max + dt.bonus_pdv_phy + dt.bonus_pdv_mag)
            dt.vie = target.vie
        if target.pdv is not None and dt.pdv is not None and int(target.pdv) > 0:
            dt.pdv = max(0, dt.pdv - int(target.pdv))
            dt.nb_att_sub = (dt.nb_att_sub if dt.nb_att_sub is not None else 0) + 1
            dt.course = False
        if target.vie is not None:
            dt.vie = target.vie
        if target.fatigue is not None and int(target.fatigue) > 0 and Being.is_mob(target.att_id):
            fatigue = dt.fatigue if dt.fatigue is not None else 0
            dt.fatigue = max(127, fatigue + int(target.fatigue))
        if target.rm is not None and int(target.rm) > 0:
            dt.base_rm_min = (dt.base_rm_min if dt.base_rm_min is not None else 0) + int(target.rm)
            dt.base_rm_max = (dt.base_rm_max if dt.base_rm_max is not None else 0) + int(target.rm)
        dt.immobile = 'glue' in t
        dt.terre = 'balayage' in t and not target.esquive
        sg.db.upsert(dt)


@event.listens_for(battleEvent, 'after_insert')
def link_follower(mapper, connection, target):
    beings = [target.att_id, target.def_id, target.autre_id]
    if not any(target.owner_id == being_id for being_id in beings):
        # Owner of the event is not any of the being involved, event is related to a follower
        # Since follower are mobs and no mob can hurt another mob: find the unique mob being involved
        # If several mobs, then either we messed up or MH changed the rules
        followers = list(filter(lambda x : x is not None and Mob.is_mob(x), beings))
        if len(followers) == 1:
            follower = sg.db.session.query(MobPrivate).get((followers[0], target.owner_id))
            if follower is not None:
                follower.owner_id = target.owner_id
                sg.db.upsert(follower)
