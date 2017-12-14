#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import ConfigParser
from sqlalchemy import create_engine, exc, orm, inspect, event, and_
from sqlalchemy_utils import database_exists, create_database
from classes.user import USER
from classes.troll import TROLL
from classes.metamob import METAMOB
from classes.mob import MOB
from classes.cdm import CDM
from classes.battle import BATTLE
from classes.event import EVENT
from classes.hook import HOOK
from classes.piege import PIEGE
from classes.conf import CONF
from classes.group import GROUP
from classes.portal import PORTAL
import modules.globals as sg

## SCIZ SQL Help

class SQLHelper:

    # Constructor
    def __init__(self):
        self.check_conf()
        self.connect()

    # Configuration loader and checker
    def check_conf(self):
        try:
            # Load DB conf
            self.db_host = sg.config.get(sg.CONF_DB_SECTION, sg.CONF_DB_HOST)
            self.db_port = sg.config.get(sg.CONF_DB_SECTION, sg.CONF_DB_PORT)
            self.db_name = sg.config.get(sg.CONF_DB_SECTION, sg.CONF_DB_NAME)
            self.db_user = sg.config.get(sg.CONF_DB_SECTION, sg.CONF_DB_USER)
            self.db_pass = sg.config.get(sg.CONF_DB_SECTION, sg.CONF_DB_PASS)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error('Fail to load config! (ConfigParser error: %s)' % (str(e), ))
            raise

    # Init the DB
    def init(self):
        try:
            sg.SqlAlchemyBase.metadata.create_all(self.engine)
        except (exc.SQLAlchemyError, exc.DBAPIError) as e:
            e.sciz_logger_flag = True
            sg.logger.error('Fail to init the DB! (SQLAlchemy error: %s)' % (str(e), ))
            raise
    
    # Connect to the DB
    def connect(self):
        try:
            db_url = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (self.db_user, self.db_pass, self.db_host, self.db_port, self.db_name, )
            self.engine = create_engine(db_url, encoding=sg.DEFAULT_CHARSET)
            if self.db_name and not database_exists(self.engine.url):
                create_database(self.engine.url)
            self.sessionMaker = orm.sessionmaker(bind=self.engine)
            self.session = self.sessionMaker()
        except (exc.SQLAlchemyError, exc.DBAPIError) as e:
            e.sciz_logger_flag = True
            sg.logger.error('Fail to conect to the DB! (SQLAlchemy error: %s)' % (str(e), ))
            raise

    # Add any object (dispatcher)
    def add(self, obj, obj2=None):
        if isinstance(obj, MOB):
            return self.__add_mob(obj)
        elif isinstance(obj, CDM):
            return self.__add_cdm(obj)
        elif isinstance(obj, PIEGE):
            return self.__add_piege(obj)
        elif isinstance(obj, PORTAL):
            return self.__add_portal(obj)
        elif isinstance(obj, TROLL):
            return self.__add_troll(obj, obj2)
        elif isinstance(obj, BATTLE):
            return self.__add_battle(obj)
        elif isinstance(obj, USER):
            return self.__add_user(obj)
        elif isinstance(obj, GROUP):
            return self.__add_group(obj)
        elif isinstance(obj, CONF):
            return self.__add_conf(obj)

    # Insert or update a USER
    def __add_user(self, new_user):
        user = None
        try:
            old_user = self.session.query(USER).filter(USER.id == new_user.id).one() 
            user = self.session.merge(new_user)
            sg.logger.info('Updating user %s...' % (user.id, ))
        except orm.exc.NoResultFound:
            user = new_user
            sg.logger.info('Creating user %s...' % (user.id, ))
        self.session.add(user)
        self.session.commit()
        return user
    
    # Add a TROLL
    def __add_troll(self, new_troll, battle=None):
        troll = None
        try:
            troll = self.session.query(TROLL).filter(and_(TROLL.id == new_troll.id, TROLL.group_id == new_troll.group_id)).one()
            sg.logger.info("Updating troll %s..." % (troll.id, ))
            troll.update_from_new(new_troll, battle)
        except orm.exc.NoResultFound:
            troll = new_troll
            sg.logger.info("Creating troll %s..." % (troll.id, ))
        self.session.add(troll)
        self.session.commit()
        return troll
            
    # Add a CONF
    def __add_conf(self, new_conf):
        conf = None
        try:
            conf = self.session.query(CONF).filter(and_(CONF.key == new_conf.key, CONF.section == new_conf.section, CONF.group_id == new_conf.group_id)).one() 
            # sg.logger.info('Updating conf %s for group %s...' % (new_conf.key, new_conf.group_id, ))
            conf.value = new_conf.value
            self.session.add(conf)
        except orm.exc.NoResultFound:
            sg.logger.info('Creating conf %s for group %s...' % (new_conf.key, new_conf.group_id, ))
            conf = new_conf
        self.session.add(conf) 
        self.session.commit()
        return conf
    
    # Add a GROUP
    def __add_group(self, new_group):
        group = None
        try:
            group = self.session.query(GROUP).filter(GROUP.id == new_group.id).one()
            sg.logger.info('Updating group %s...' % (group.name, ))
        except orm.exc.NoResultFound:
            group = new_group
            sg.logger.info('Creatin group %s...' % (group.name, ))
        self.session.add(group)
        self.session.commit()
        return group

    # Add an EVENT
    def add_event(self, obj):
        event = EVENT()
        event.group_id = obj.group_id
        event.time = obj.time
        event.notif = sg.pretty_print(obj, True)
        event.notif_to_push = False
        event.type = "UNKNWON"
        if isinstance(obj, CDM):
            if (obj.mob.sciz_notif or obj.troll.sciz_notif):
                event.notif_to_push = True
            event.cdm_id = obj.id
            event.type = "CDM"
        elif isinstance(obj, PIEGE):
            if (obj.troll.sciz_notif):
                event.notif_to_push = True
            event.piege_id = obj.id
            event.type = "PIEGE"
        elif isinstance(obj, PORTAL):
            if (obj.troll.sciz_notif):
                event.notif_to_push = True
            event.portal_id = obj.id
            event.type = "PORTAL"
        elif isinstance(obj, BATTLE):
            if ((obj.att_troll != None and obj.att_troll.sciz_notif) or (obj.att_mob != None and obj.att_mob.sciz_notif) or (obj.def_troll != None and obj.def_troll.sciz_notif) or (obj.def_mob != None and obj.def_mob.sciz_notif)):
                event.notif_to_push = True
            event.battle_id = obj.id
            event.type = "BATTLE"
        self.session.add(event)
        self.session.commit()
        return event
        
    # Add a MOB
    def __add_mob(self, new_mob):
        mob = None
        try:
            mob = self.session.query(MOB).filter(and_(MOB.id == new_mob.id, MOB.group_id == new_mob.group_id)).one()
            sg.logger.info("Updating mob %s..." % (mob.id, ))
            mob.update_from_new(new_mob)
            if mob.metamob_id is None:
                mob.link_metamob(self.session.query(METAMOB).all())
            self.session.add(mob)
        except orm.exc.NoResultFound:
            mob = new_mob
            sg.logger.info("Creating MOB %s..." % (mob.id, ))
            mob.sciz_notif = True
            mob.link_metamob(self.session.query(METAMOB).all())
        self.session.add(mob)
        self.session.commit()
        return mob

    # Add a PIEGE
    def __add_piege(self, piege):
        troll = TROLL()
        troll.id = piege.troll_id
        troll.group_id = piege.group_id
        self.__add_troll(troll)
        self.session.add(piege)
        self.session.commit()
        return piege
    
    # Add a PORTAL
    def __add_portal(self, portal):
        troll = TROLL()
        troll.id = portal.troll_id
        troll.group_id = portal.group_id
        self.__add_troll(troll)
        try:
            portal = self.session.query(PORTAL).filter(PORTAL.id == portal.id).one()
            sg.logger.warning('The portal %s already exists, aborting...' % (portal.id))
            return None
        except orm.exc.NoResultFound:
            self.session.add(portal)
            self.session.commit()
        return portal

    # Add a CDM
    def __add_cdm(self, cdm):
        mob = MOB()
        mob.populate_from_cdm(cdm)
        self.__add_mob(mob)
        troll = TROLL()
        troll.id = cdm.troll_id
        troll.group_id = cdm.group_id
        self.__add_troll(troll)
        self.session.add(cdm)
        self.session.commit()
        return cdm
    
    # Add a BATTLE
    def __add_battle(self, battle):
        if battle.att_troll_id != None:
            att_troll = TROLL()
            att_troll.id = battle.att_troll_id
            att_troll.group_id = battle.group_id
            att_troll.nom = battle.att_troll_nom
            self.__add_troll(att_troll, battle)
        if battle.def_troll_id != None:
            def_troll = TROLL()
            def_troll.id = battle.def_troll_id
            def_troll.group_id = battle.group_id
            def_troll.nom = battle.def_troll_nom
            self.__add_troll(def_troll, battle)
        if battle.att_mob_id != None:
            att_mob = MOB()
            att_mob.id = battle.att_mob_id
            att_mob.group_id = battle.group_id
            att_mob.nom = battle.att_mob_nom
            att_mob.age = battle.att_mob_age
            att_mob.tag = battle.att_mob_tag
            self.__add_mob(att_mob)
        if battle.def_mob_id != None:
            def_mob = MOB()
            def_mob.id = battle.def_mob_id
            def_mob.group_id = battle.group_id
            def_mob.nom = battle.def_mob_nom
            def_mob.age = battle.def_mob_age
            def_mob.tag = battle.def_mob_tag
            self.__add_mob(def_mob)
        self.session.add(battle)
        self.session.commit()
        return battle
    
    # Prevent the update of attrs to None
    @event.listens_for(TROLL, 'before_update')
    @event.listens_for(USER, 'before_update')
    @event.listens_for(METAMOB, 'before_update')
    @event.listens_for(MOB, 'before_update')
    @event.listens_for(CDM, 'before_update')
    @event.listens_for(BATTLE, 'before_update')
    @event.listens_for(PIEGE, 'before_update')
    @event.listens_for(PORTAL, 'before_update')
    @event.listens_for(GROUP, 'before_update')
    @event.listens_for(HOOK, 'before_update')
    def before_udpate(mapper, connection, target):
        state = inspect(target)
        for attr in state.attrs:
            hist = state.get_history(attr.key, True)
            if hist.has_changes() and not hist.added[0]:
                setattr(target, attr.key, hist.deleted[0])
    
    # Destructor
    def __del__(self):
        if self.engine:
            self.engine.dispose()
