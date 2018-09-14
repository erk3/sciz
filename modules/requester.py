#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import ConfigParser, sqlalchemy, math
from operator import attrgetter, add
from sqlalchemy import desc, asc, or_, and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from classes.troll import TROLL
from classes.user import USER
from classes.mob import MOB
from classes.cdm import CDM
from classes.aa import AA
from classes.battle import BATTLE
from modules.mh_caller import MHCaller
from modules.sql_helper import SQLHelper
import modules.globals as sg

## Requester class for SCIZ
class Requester:

    # Constructor
    def __init__(self):
        self.check_conf()
        self.mhCaller = MHCaller()
    
    # Configuration loader and checker
    def check_conf(self):
        # No conf needed yet
        pass

    # Dispatcher
    def request(self, ids, args):
        # Request on all trolls
        ids = ids.lower()
        if ids == 'trolls' or ids == 'users':
            trolls = sg.db.session.query(TROLL).filter(TROLL.group_id==sg.group.id).all()
            if ids == 'users':
                trolls = filter(lambda x : x.user != None, trolls)
            if len(args) == 1:
                trolls = sorted(trolls, key=lambda x : sg.none_sorter(x, args[0])) # Work only if args == only an object attr (ex:'dla' ; not 'dla,pv' or 'event')
            for troll in trolls:
                self.__request_troll(troll.id, args)
        else:
            id_lst = ids.split(',')
            is_mob_lst = is_troll_lst = True
            for id in id_lst:
                is_troll_lst = is_troll_lst and (len(id) <= 6 and id.isdigit())
                is_mob_lst = is_mob_lst and (len(id) == 7 and id.isdigit())
            # Request on a specific list of mobs
            if is_mob_lst and not is_troll_lst:
                for id in id_lst:
                    self.__request_mob(id, args)
            # Request on a specific list of trolls
            elif is_troll_lst and not is_mob_lst:
                for id in id_lst:
                    self.__request_troll(id, args)
            # Request on an inconsitant list of ids
            else:
                print 'Inconsistant list of ids...'

    # Mob request
    def __request_mob(self, id, args):
        if len(args) > 0:
            limit = 1
            if len(args) > 1 and args[1].isdigit():
                limit = int(args[1]) if int(args[1]) > 0 else limit
            if args[0].lower() == 'cdm':
                self.__request_mob_cdm(id, limit)
            elif args[0].lower() == 'event':
                self.__request_mob_event(id, limit)
            elif args[0].lower() == 'recap':
                self.__request_mob_recap(id)
            else:
                caracs = args[0].split(',')
                self.__request_mob_caracs(id, caracs)
        else:
            self.__request_mob_caracs(id, None)

    def __request_mob_recap(self, id):
        try:
            # Data pull from DB
            mob = sg.db.session.query(MOB).filter(MOB.group_id==sg.group.id, MOB.id == id).one()
            # cdms = sg.db.session.query(CDM).filter(CDM.mob_id==id, CDM.group_id==sg.group.id).order_by(desc(CDM.time)).all()
            try:
                cdm = sg.db.session.query(CDM).filter(CDM.mob_id==id, CDM.group_id==sg.group.id).order_by(desc(CDM.time)).first()
            except NoResultFound:
                cdm = None
            if cdm:
                battles = sg.db.session.query(BATTLE).filter(and_(BATTLE.group_id==sg.group.id, or_(BATTLE.att_mob_id == id, BATTLE.def_mob_id == id), BATTLE.time > cdm.time)).order_by(asc(BATTLE.time)).all()
            else:
                battles = sg.db.session.query(BATTLE).filter(and_(BATTLE.group_id==sg.group.id, or_(BATTLE.att_mob_id == id, BATTLE.def_mob_id == id))).order_by(asc(BATTLE.time)).all()
            #events = sorted(cdm + battles, key=attrgetter('time'))
            # Vars
            ptime = None
            is_dead = False
            tot = 0
            pv_min = mob.pv_min
            pv_max = mob.pv_max
            reg_min = mob.reg_min * 1 if mob.reg_min else (mob.reg_max * 1 if mob.reg_max else None)
            reg_max = mob.reg_max * 3 if mob.reg_max else (mob.reg_min * 3 if mob.reg_min else None)
            tot_reg_min = tot_reg_max = 0
            # Recap compute
            if cdm:
                if pv_min: pv_min = int(math.ceil(float(100 - cdm.blessure) / 100 * mob.pv_min))
                if pv_max: pv_max = int(math.floor(float(100 - cdm.blessure) / 100 * mob.pv_max))

            for battle in battles:
                if battle.def_mob_id is not None and battle.pv > 0:
                    is_dead = battle.dead
                    ptime = battle.time if ptime is None or battle.dead else ptime
                    tot += battle.pv
                    if pv_min is not None: pv_min -= battle.pv
                    if pv_max is not None: pv_max -= battle.pv
                if battle.att_mob_id is not None:
                    if reg_min is not None: tot_reg_min += reg_min
                    if reg_max is not None: tot_reg_max += reg_max
            # Pretty print
            print ("%s [%s] (%d)" % (mob.nom, mob.age, mob.id)).encode(sg.DEFAULT_CHARSET)
            if cdm and not is_dead:
                print "Dernière CDM : %d%%  (%s)" % (cdm.blessure, cdm.time,)
            if tot != 0 and not is_dead:
                print "Total depuis %s : -%d PV %s" % ("" if cdm else ptime, tot, "(MORT)" if is_dead else "",)
            if not is_dead:
                if pv_min is not None or pv_max is not None:
                    print "PdV restants : %s" % (sg.str_min_max(max(pv_min, 1), pv_max),)
                if tot_reg_min or tot_reg_max:
                    print "PdV régénérés : %s" % (sg.str_min_max(tot_reg_min, tot_reg_max),)
            else:
                print "Tué le %s" % (ptime,)
        except NoResultFound:
            print 'Aucune donnée pour le monstre n°%s' % (id, )

    def __request_mob_cdm(self, id, limit):
        try:        
            cdms = sg.db.session.query(CDM).filter(CDM.mob_id==id, CDM.group_id==sg.group.id).order_by(desc(CDM.time)).limit(limit).all()
            i = len(cdms) - 1
            if i >= 0:
                while i >= 0:
                    val = sg.pretty_print(cdms[i], False, None)
                    if val != '':
                        print val
                    i -= 1
            else:
                print 'Aucune CDM pour le montre n°%s' % (id, )
        except NoResultFound:
            print 'Aucune CDM pour le monstre n°%s' % (id, )
    
    def __request_mob_event(self, id, limit):
        try:
            events = sg.db.session.query(BATTLE).filter(and_(BATTLE.group_id==sg.group.id, or_(BATTLE.att_mob_id == id, BATTLE.def_mob_id == id))).order_by(desc(BATTLE.time)).limit(limit).all()
            i = len(events) - 1
            if i >= 0:
                while i >= 0:
                    val = sg.pretty_print(events[i], False, None)
                    if val != '':
                        print val
                    i -= 1
            else:
                print 'Aucun évènement pour le monstre n°%s' % (id, )
        except NoResultFound:
            print 'Aucun évènement pour le monstre n°%s' % (id, )
    
    def __request_mob_caracs(self, id, caracs):
        try:
            mob = sg.db.session.query(MOB).filter(MOB.group_id==sg.group.id, MOB.id == id).one()
            val = sg.pretty_print(mob, False, caracs)
            if val != '':
                print val
            else:
                print 'Aucune donnée pour le monstre n°%s' % (id, )
        except NoResultFound:
            print 'Aucune donnée pour le monstre n°%s' % (id, )
    
    # Trol request        
    def __request_troll(self, id, args):
        if len(args) > 0:
            limit = 1
            if len(args) > 1 and args[1].isdigit():
                limit = int(args[1]) if int(args[1]) > 0 else limit
            if args[0].lower() == 'event':
                self.__request_troll_event(id, limit)
            elif args[0].lower() == 'aa':
                self.__request_troll_aa(id, limit)
            elif args[0].lower() == 'recap':
                self.__request_troll_recap(id)
            elif args[0].lower() == 'update':
                self.__request_troll_update(id)
            else:
                caracs = args[0].split(',')
                self.__request_troll_caracs(id, caracs)
        else:
            self.__request_troll_caracs(id, None)
    
    def __request_troll_recap(self, id):
        pass
    
    def __request_troll_update(self, id):
        # The third parameter 'verbose' handles the output
        self.mhCaller.call('vue2', [id], False)
        self.mhCaller.call('profil4', [id], True)

    def __request_troll_aa(self, id, limit):
        try:        
            aas = sg.db.session.query(AA).filter(AA.troll_cible_id==id, AA.group_id==sg.group.id).order_by(desc(AA.time)).limit(limit).all()
            i = len(aas) - 1
            if i >= 0:
                while i >= 0:
                    val = sg.pretty_print(aas[i], False, None)
                    if val != '':
                        print val
                    i -= 1
            else:
                print 'Aucune AA pour le troll n°%s' % (id, )
        except NoResultFound:
            print 'Aucune AA pour le troll n°%s' % (id, )

    def __request_troll_event(self, id, limit):
        try:
            events = sg.db.session.query(BATTLE).filter(and_(BATTLE.group_id==sg.group.id, or_(BATTLE.att_troll_id == id, BATTLE.def_troll_id == id))).order_by(desc(BATTLE.time)).limit(limit).all()
            i = len(events) - 1
            if i >= 0:
                while i >= 0:
                    val = sg.pretty_print(events[i], False, None)
                    if val != '':
                        print val
                    i -= 1
            else:
                print 'Aucun évènement pour troll n°%s' % (id, )
        except NoResultFound:
            print 'Aucun évènement pour troll n°%s' % (id, )

    def __request_troll_caracs(self, id, caracs):
        try:
            troll = sg.db.session.query(TROLL).filter(TROLL.group_id==sg.group.id, TROLL.id == id).one()
            val = sg.pretty_print(troll, False, caracs)
            if val != '':
                print val
            else:
                print 'Aucune donnée pour le troll n°%s' % (id, )
        except NoResultFound:
            print 'Aucune donnée pour le troll n°%s' % (id, )

    # Destructor
    def __del__(self):
        pass
