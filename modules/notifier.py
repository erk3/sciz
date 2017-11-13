#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import ConfigParser, sqlalchemy, os
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from modules.sql_helper import SQLHelper
from classes.event import EVENT
from classes.hook import HOOK
import modules.globals as sg

## Notifier class for SCIZ
class Notifier:

    # Constructor
    def __init__(self):
        self.check_conf()
    
    # Configuration loader and checker
    def check_conf(self):
        # No conf needed yet
        pass

    # Print all the notifications on stdout and set the new last event id for the hook
    def print_flush(self, hook_name):
        try:
            hook = sg.db.session.query(HOOK).filter(HOOK.name == hook_name, HOOK.group_id==sg.group.id).one()
            for event in sg.db.session.query(EVENT).filter(EVENT.id > hook.last_event_id, EVENT.notif_to_push == True, EVENT.group_id==sg.group.id):
                print event.notif.encode(sg.DEFAULT_CHARSET) + os.linesep
                hook.last_event_id = event.id
            sg.db.session.add(hook)
            sg.db.session.commit()
        except NoResultFound:
            sg.logger.warning('No hook or no events found matching the request...')

    # Destructor
    def __del__(self):
        pass
