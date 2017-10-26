#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import ConfigParser, sqlalchemy, os
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from modules.sql_helper import SQLHelper
from classes.event import EVENT
from classes.hook import HOOK
import modules.globals as sg

## Notifier class for SCIZ
class Notifier:

    # Constructor
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.check_conf()
        self.sqlHelper = SQLHelper(config, logger)
    
    # Configuration loader and checker
    def check_conf(self):
        # No conf needed yet
        pass

    # Print all the notifications on stdout and set the new last event id for the hook
    def print_flush(self, hook_name):
        try:
            hook = self.sqlHelper.session.query(HOOK).filter(HOOK.nom == hook_name).one()
            
            for event in self.sqlHelper.session.query(EVENT).filter(EVENT.id > hook.last_event_id, EVENT.notif_to_push == True):
                print event.notif.encode(sg.DEFAULT_CHARSET) + os.linesep
                hook.last_event_id = event.id

            self.sqlHelper.session.add(hook)
            self.sqlHelper.session.commit()

        except NoResultFound:
            pass

    # Set all the notification as pushed
    def flush(self):
        for event in self.sqlHelper.session.query(EVENT).filter(EVENT.notif_to_push == True):
            event.notif_to_push = False
            self.sqlHelper.session.add(event)
        self.sqlHelper.session.commit()

    # Destructor
    def __del__(self):
        pass
