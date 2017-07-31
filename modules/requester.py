#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import ConfigParser, sqlalchemy
from sqlalchemy import desc, or_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from classes.mob import MOB
from classes.cdm import CDM
from classes.battle_event import BATTLE_EVENT
from modules.sql_helper import SQLHelper
from modules.pretty_printer import PrettyPrinter
import modules.globals as sg

## Requester class for SCIZ
class Requester:

    # Constructor
    def __init__(self, config):
        self.config = config
        self.check_conf()
        self.sqlHelper = SQLHelper(config)
        self.pprinter = PrettyPrinter(config)
    
    # Configuration loader and checker
    def check_conf(self):
        # No conf needed yet
        pass

    def request(self, entity, args):
        if entity == 'mob':
            self.__request_mob(args)
        elif entity == 'troll':
            self.__request_troll(args)

    def __request_mob(self, args):
        ids = args[0].split(',')
        l = len(args)
        # if the * was forgotten
        if l == 1:
            args.append('*')
        # last_cdm
        if args[1].lower() == 'last_cdm':
            self.__request_mob_last_cdm(ids) 
        # last_event
        elif args[1].lower() == 'last_event':
            # with a valid limit
            if l < 3 or not args[2].isdigit():
                args.append(5)
            self.__request_mob_last_event(ids, int(args[2])) 
        # caracs
        else:
            caracs = None if args[1] == '*' else args[1].split(',')
            self.__request_mob_caracs(ids, caracs)
    
    def __request_mob_last_cdm(self, ids):
        for id in ids:
            try:
                cdm = self.sqlHelper.session.query(CDM).filter(CDM.mob_id == id).order_by(desc(CDM.time)).limit(1).one()
                print self.pprinter.pretty_print(cdm, False)
            except NoResultFound:
                pass
    
    def __request_mob_last_event(self, ids, limit):
        for id in ids:
            try:
                events = self.sqlHelper.session.query(BATTLE_EVENT).filter(or_(BATTLE_EVENT.att_mob_id == id, BATTLE_EVENT.def_mob_id == id)).order_by(desc(BATTLE_EVENT.time)).limit(limit).all()
                for event in events:
                    print self.pprinter.pretty_print(event, False)
            except NoResultFound:
                pass
    
    def __request_mob_caracs(self, ids, caracs):
        if not caracs: 
            for id in ids:
                try:
                    mob = self.sqlHelper.session.query(MOB).filter(MOB.id == id).one()
                    print self.pprinter.pretty_print(mob, False)
                except NoResultFound:
                    pass
            
        else:
            # FIXME : filter out stats (in pprint ?)
            pass

    def __request_troll(self, args):
        pass

    # Destructor
    def __del__(self):
        pass
