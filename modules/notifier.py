#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import ConfigParser, sqlalchemy, os
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from modules.sql_helper import SQLHelper
from classes.notif import NOTIF
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

    # Print all the notifications on stdout
    def print_all(self):
        for notif in self.sqlHelper.session.query(NOTIF).filter(NOTIF.to_push == True):
            print notif.text.encode(sg.DEFAULT_CHARSET) + os.linesep

    # Set all the notification as pushed
    def flush(self):
        for notif in self.sqlHelper.session.query(NOTIF).filter(NOTIF.to_push == True):
            notif.to_push = False
            self.sqlHelper.session.add(notif)
        self.sqlHelper.session.commit()

    # Destructor
    def __del__(self):
        pass
