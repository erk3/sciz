#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import sys, ConfigParser, sqlalchemy, json, codecs
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sciz_sql_helper import SQLHelper
from sciz_user_class import USER
import sciz_globals as sg

## AdminHelper class for SCIZ
class AdminHelper:

    # Constructor
    def __init__(self, config):
        self.config = config
        self.check_conf()
        self.sqlHelper = SQLHelper(config)
    
    # Configuration loader and checker
    def check_conf(self):
        try:
            self.json_users_tag = self.config.get(sg.CONF_JSON_SECTION, sg.CONF_JSON_USERS_TAG)
            self.json_users_id = self.config.get(sg.CONF_JSON_SECTION, sg.CONF_JSON_USERS_ID)
        except ConfigParser.Error as e:
            print('Fail to load config file! (ConfigParser error:' + str(e) + ')')
            raise

    # Initializer, instancites the SQL schema
    def init(self):
        self.sqlHelper.init()
    
    # Users updater from JSON file
    def update_users(self, json_file):
        with codecs.open(json_file, 'r', sg.DEFAULT_CHARSET) as f:
            data = json.load(f)
            for u in data[self.json_users_tag]:
                user = USER()
                user.update_from_json(u, True)
                self.sqlHelper.add(user)
            self.sqlHelper.session.commit()

    # Destructor
    def __del__(self):
        pass
