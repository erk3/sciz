#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import ConfigParser, sqlalchemy
from operator import attrgetter
from sqlalchemy import desc, or_, and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from classes.troll import TROLL
from classes.user import USER
from classes.mob import MOB
from classes.cdm import CDM
from classes.battle import BATTLE
from modules.sql_helper import SQLHelper
from modules.pretty_printer import PrettyPrinter
import modules.globals as sg

## Requester class for SCIZ
class Requester:

    # Constructor
    def __init__(self):
        self.pp = PrettyPrinter()
        self.check_conf()
    
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
                sg.logger.error('Inconsistant list of ids...')

    # Mob request
    def __request_mob(self, id, args):
        if len(args) > 0:
            limit = 1
            if len(args) > 1 and args[1].isdigit():
                limit = int(args[1])
            if args[0].lower() == 'cdm':
                self.__request_mob_cdm(id, limit)
            elif args[0].lower() == 'event':
                self.__request_mob_event(id, limit)
            else:
                caracs = args[0].split(',')
                self.__request_mob_caracs(id, caracs)
        else:
            self.__request_mob_caracs(id, None)

    def __request_mob_cdm(self, id, limit):
        try:        
            cdms = sg.db.session.query(CDM).filter(CDM.mob_id==id, CDM.group_id==sg.group.id).order_by(desc(CDM.time)).limit(limit).all()
            for cdm in cdms:
                val = self.pp.pretty_print(cdm, False, None)
                if val != '':
                    print val
        except NoResultFound:
            pass
    
    def __request_mob_event(self, id, limit):
        try:
            events = sg.db.session.query(BATTLE).filter(and_(BATTLE.group_id==sg.group.id, or_(BATTLE.att_mob_id == id, BATTLE.def_mob_id == id))).order_by(desc(BATTLE.time)).limit(limit).all()
            for event in events:
                val = self.pp.pretty_print(event, False, None)
                if val != '':
                    print val
        except NoResultFound:
            pass
    
    def __request_mob_caracs(self, id, caracs):
        try:
            mob = sg.db.session.query(MOB).filter(MOB.group_id==sg.group.id, MOB.id == id).one()
            val = self.pp.pretty_print(mob, False, caracs)
            if val != '':
                print val
        except NoResultFound:
            pass
    
    # Trol request        
    def __request_troll(self, id, args):
        if len(args) > 0:
            limit = 1
            if len(args) > 1 and args[1].isdigit():
                limit = int(args[1])
            if args[0].lower() == 'event':
                self.__request_troll_event(id, limit)
            else:
                caracs = args[0].split(',')
                self.__request_troll_caracs(id, caracs)
        else:
            self.__request_troll_caracs(id, None)
    
    def __request_troll_event(self, id, limit):
        try:
            events = sg.db.session.query(BATTLE).filter(and_(BATTLE.group_id==sg.group.id, or_(BATTLE.att_troll_id == id, BATTLE.def_troll_id == id))).order_by(desc(BATTLE.time)).limit(limit).all()
            for event in events:
                val = self.pp.pretty_print(event, False, None)
                if val != '':
                    print val
        except NoResultFound:
            pass

    def __request_troll_caracs(self, id, caracs):
        try:
            troll = sg.db.session.query(TROLL).filter(TROLL.group_id==sg.group.id, TROLL.id == id).one()
            val = self.pp.pretty_print(troll, False, caracs)
            if val != '':
                print val
        except NoResultFound:
            pass

    # Destructor
    def __del__(self):
        pass
