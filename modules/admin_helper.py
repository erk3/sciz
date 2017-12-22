#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import sys, ConfigParser, sqlalchemy, json, codecs, datetime, os, unidecode
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from modules.mh_caller import MHCaller
from modules.mail_walker import MailWalker
from classes.user import USER
from classes.conf import CONF
from classes.group import GROUP
from classes.troll import TROLL
from classes.hook import HOOK
from classes.assoc_users_groups import AssocUsersGroups
import modules.globals as sg

## AdminHelper class for SCIZ
class AdminHelper:

    # Constructor
    def __init__(self):
        self.check_conf()
    
    # Configuration loader and checker
    def check_conf(self):
        try:
            self.json_users_tag = sg.config.get(sg.CONF_JSON_SECTION, sg.CONF_JSON_USERS_TAG)
            self.json_users_id = sg.config.get(sg.CONF_JSON_SECTION, sg.CONF_JSON_USERS_ID)
            self.domain_name = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DOMAIN_NAME)
            self.pf_conf_file = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_POSTFIX_CONF_FILE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error('Fail to load config file! (ConfigParser error: %s)' % (str(e), ))
            raise

    # Initializer, instanciates the SQL schema
    def init(self):
        sg.db.init()
        # Populate default conf for the instance
        for (each_key, each_value) in sg.config.items(sg.CONF_INSTANCE_SECTION):
            conf = CONF()
            conf.section = sg.CONF_INSTANCE_SECTION
            conf.key = each_key
            conf.value = each_value
            sg.db.add(conf)

    # Set a working group, create it in database if necessary and load its conf
    def set_group(self, group_name):
        # Set the working group
        sg.group = None
        if not isinstance(group_name, unicode):
            group_name = group_name.decode(sg.DEFAULT_CHARSET)
        flat_name = filter(str.isalnum, unidecode.unidecode(group_name.lower()))
        sg.logger.info('Group has been set to %s!' % (flat_name, ))
        try:
            sg.group = sg.db.session.query(GROUP).filter(GROUP.flat_name == flat_name).one() 
            try:
                # Group exists, push any missing configuration
                self.__push_group_conf(sg.group, False)
                # Group exists, load its configuration
                confs = sg.db.session.query(CONF).filter(CONF.group_id == sg.group.id).all()
                for conf in confs:
                    sg.config.set(conf.section, conf.key, conf.value)
                sg.logger.info('Loaded stored configurations for group %s!' % (sg.group.name, ))
            except NoResultFound as e:
                sg.logger.warning('No stored configurations found for group %s!' % (sg.group.name, ))
        except NoResultFound as e:
            # Group does not exist, create it
            sg.logger.info('Creating group %s on the fly...' % (group_name, ))
            sg.group = GROUP()
            sg.group.name = group_name
            sg.group.flat_name = flat_name
            sg.group.generate_random_mail(self.domain_name)
            sg.group = sg.db.add(sg.group)
            # Add an entry to the postfix accounts conf file
            sg.createDirName(self.pf_conf_file);
            with codecs.open(self.pf_conf_file, 'a', sg.DEFAULT_CHARSET) as fp:
                fp.write("%s|%s\n" % (sg.group.mail, sg.group.mail_pwd, ))
            self.__push_group_conf(sg.group, False)

    def reset_groups_conf(self, group_name=None):
        if group_name and isinstance(group_name, str) and group_name != '':
            if not isinstance(group_name, unicode):
                group_name = group_name.decode(sg.DEFAULT_CHARSET)
            flat_name = filter(str.isalnum, unidecode.unidecode(group_name.lower()))
            sg.logger.info('Reseting conf for group %s...' % flat_name)
            try:
                group = sg.db.session.query(GROUP).filter(GROUP.flat_name == flat_name).one()
                self.__push_group_conf(group, True)
            except NoResultFound as e:
                sg.logger.warning('No group %s, aborting reset confs...' % (flat_name))
        else:
            sg.logger.info('Reseting conf for all groups...')
            groups = sg.db.session.query(GROUP).all()
            for group in groups:
                self.__push_group_conf(group, True)

    # Routine for pushing conf to a group
    def __push_group_conf(self, group, force=False):
        for section in [sg.CONF_GROUP_BATTLE_FORMAT, sg.CONF_GROUP_TROLL_FORMAT, sg.CONF_GROUP_MOB_FORMAT, sg.CONF_GROUP_CDM_FORMAT, sg.CONF_GROUP_PIEGE_FORMAT, sg.CONF_GROUP_PORTAL_FORMAT]:
            if sg.config.has_section(section):
                for (each_key, each_value) in sg.config.items(section):
                    conf = CONF()
                    to_add = False
                    if not force:
                        try:
                            conf = sg.db.session.query(CONF).filter(CONF.group_id == group.id, CONF.section == section, CONF.key == each_key).one()
                        except NoResultFound as e:
                            to_add = True
                    if to_add or force:
                        conf.section = section
                        conf.key = each_key
                        conf.value = each_value
                        conf.group_id = group.id
                        conf.touch()
                        sg.db.add(conf)

    # Create or update users from JSON file, then if a group is set also do the binding and create the troll
    def add_json_users(self, json_file):
        with codecs.open(json_file, 'r', sg.DEFAULT_CHARSET) as f:
            data = json.load(f)
            for u in data[self.json_users_tag]:
                user = USER()
                user.build_from_json(u)
                role = user.role if hasattr(user, 'role') and user.role else 1
                user = sg.db.add(user)
                if sg.group:
                    try:
                        assoc = sg.db.session.query(AssocUsersGroups).filter(AssocUsersGroups.user_id == user.id, AssocUsersGroups.group_id == sg.group.id).one()
                        assoc.role = role
                    except NoResultFound as e:
                        assoc = AssocUsersGroups(user_id=user.id, group_id=sg.group.id, role=role);
                        user.groups.append(assoc)
                    user.pwd = None # Required for avoiding double hashing
                    sg.db.add(user)
                    troll = TROLL()
                    troll.id = user.id
                    troll.user_id = user.id
                    troll.group_id = sg.group.id
                    sg.db.add(troll)

    def auto_tasks(self):
        self.__auto_task_check(sg.CONF_INSTANCE_FTP_REFRESH, self.__auto_task_mh_ftp_call)
        self.__auto_task_check(sg.CONF_INSTANCE_MAIL_REFRESH, self.__auto_task_mail_walk)
        self.__auto_task_check(sg.CONF_INSTANCE_MAIL_RETENTION, self.__auto_task_mail_purge)
        self.__auto_task_check(sg.CONF_INSTANCE_HOOK_REFRESH, self.__auto_task_hook_push)
        self.__auto_task_per_user_check()

    def __auto_task_per_user_check(self):
        users = sg.db.session.query(USER).all()
        users_dyn_sp = []
        users_static_sp = []
        sg.logger.info('Checking if an SP refresh is needed for each user...')
        for user in users:
            if user.dyn_sp_refresh:
                if not user.last_dyn_sp_call or ((datetime.datetime.utcnow() - user.last_dyn_sp_call).total_seconds() >= (user.dyn_sp_refresh * 60)):
                    user.last_dyn_sp_call = datetime.datetime.utcnow()
                    users_dyn_sp.append(user)
            if user.static_sp_refresh:
                if not user.last_static_sp_call or ((datetime.datetime.utcnow() - user.last_static_sp_call).total_seconds() >= (user.static_sp_refresh * 60)):
                    user.last_static_sp_call = datetime.datetime.utcnow()
                    users_static_sp.append(user)
            sg.db.add(user)
        mh = MHCaller()
        if len(users_dyn_sp) > 0:
            for user in users_dyn_sp:
                sg.logger.info('Calling Profil2 MH SP for %s...', (user.id, ))
                mh.profil2_sp_call(user)
                sg.logger.info('Calling Caract MH SP for %s...', (user.id, ))
                mh.caract_sp_call(user)
        if len(users_static_sp) > 0:
            pass
    
    def __auto_task_check(self, conf_key, callback):
        sg.logger.info('Checking if a %s is needed for the instance...' % (conf_key, ))
        conf = sg.db.session.query(CONF).filter(and_(CONF.key == conf_key, CONF.group_id == None)).one()
        if not conf.last_fetch or ((datetime.datetime.utcnow() - conf.last_fetch).total_seconds() >= (int(conf.value) * 60)):
            callback()
            conf.touch()
            sg.db.add(conf)
    
    def __auto_task_mh_ftp_call(self):
        sg.logger.info('Updating MH FTPs for all...')
        mh = MHCaller()
        mh.call('trolls2', [])
        mh.call('monstres', [])
    
    def __auto_task_mail_walk(self):
        sg.logger.info('Walking mails for all...',)
        mw = MailWalker()
        groups = sg.db.session.query(GROUP).all()
        for group in groups:
            self.set_group(group.flat_name)
            mw.walk(group)

    def __auto_task_mail_purge(self):
        sg.logger.info('Purging mails for all...',)
        mw = MailWalker()
        groups = sg.db.session.query(GROUP).all()
        for group in groups:
            self.set_group(group.flat_name)
            mw.purge(group)

    def __auto_task_hook_push(self):
        sg.logger.info('Triggering the reverse hooks for all...',)
        rhooks = sg.db.session.query(HOOK).filter(HOOK.revoked == False, HOOK.url != None).all()
        for rhook in rhooks:
            rhook.trigger()

    # Destructor
    def __del__(self):
        pass
