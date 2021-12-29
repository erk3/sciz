#!/usr/bin/env python3
#coding: utf-8

# IMPORTS
from classes.being import Being
from classes.being_troll import Troll
from classes.being_troll_private import TrollPrivate
from classes.being_troll_private_capa import TrollPrivateCapa
from classes.being_mob import Mob
from classes.being_mob_meta import MetaMob
from classes.being_mob_private import MobPrivate
from classes.tresor import Tresor
from classes.tresor_meta import MetaTresor
from classes.tresor_private import TresorPrivate
from classes.champi import Champi
from classes.champi_private import ChampiPrivate
from classes.capa_meta import MetaCapa
from classes.lieu import Lieu
from classes.lieu_portail import Portail
from classes.lieu_piege import Piege
from classes.event import Event
from classes.event_aa import aaEvent
from classes.event_cdm import cdmEvent
from classes.event_tp import tpEvent
from classes.event_cp import cpEvent
from classes.user import User
from classes.user_mh_call import MhCall
from classes.user_partage import Partage
from classes.coterie import Coterie
from classes.coterie_hook import Hook
from sqlalchemy import create_engine, orm
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql.functions import ReturnTypeFromArgs
from sqlalchemy.orm import object_session
import modules.globals as sg

class unaccent(ReturnTypeFromArgs):
    pass

# CLASS DEFINITION
class SqlHelper:

    # Constructor
    def __init__(self):
        self.load_conf()
        self.connect()

    # Configuration loader
    def load_conf(self):
        self.db_host = sg.conf[sg.CONF_DB_SECTION][sg.CONF_DB_HOST]
        self.db_port = sg.conf[sg.CONF_DB_SECTION][sg.CONF_DB_PORT]
        self.db_name = sg.conf[sg.CONF_DB_SECTION][sg.CONF_DB_NAME]
        self.db_user = sg.conf[sg.CONF_DB_SECTION][sg.CONF_DB_USER]
        self.db_pass = sg.conf[sg.CONF_DB_SECTION][sg.CONF_DB_PASS]

    # Init the DB (create the tables)
    def init(self):
        sg.sqlalchemybase.metadata.create_all(self.engine)
        sg.db.engine.execute('CREATE EXTENSION IF NOT EXISTS unaccent;')

    # Connect to the DB (create it if missing)
    def connect(self):
        db_url = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (self.db_user, self.db_pass, self.db_host, self.db_port, self.db_name)
        self.engine = create_engine(db_url, encoding=sg.DEFAULT_CHARSET, pool_recycle=3600, pool_size=25, max_overflow=10, executemany_mode='batch')
        if self.db_name is not None and not database_exists(self.engine.url):
            create_database(self.engine.url)
        # Create the session for main querying
        self.sessionMaker = orm.sessionmaker(bind=self.engine, expire_on_commit = False, autoflush=False, autocommit=False)
        self.session = orm.scoped_session(self.sessionMaker)

    # Get a fresh new session
    def new_session(self):
        return orm.scoped_session(self.sessionMaker)

    # Rebind any object to a session (no commit)
    def rebind(self, obj, given_session=None):
        #sg.logger.debug('Rebinding %s...' % obj)
        if given_session is None:
            session = object_session(obj) or self.new_session()
            obj = session.merge(obj)
        else:
            session = given_session
        obj = session.merge(obj)
        return session, obj

    # Upsert any object
    def upsert(self, obj, given_session=None, propagate=True):
        #sg.logger.debug('Upserting %s...' % obj)
        if given_session is None:
            session = self.new_session()
            obj = session.merge(obj)
            session.commit()
            session.close()
        else:
            obj = given_session.merge(obj)
        if propagate:
            self.reconciliate(obj)
        return obj

    # Upsert any Private
    def reconciliate(self, obj):
        if any(isinstance(obj, c) for c  in [TrollPrivate, MobPrivate, ChampiPrivate, TresorPrivate]):
            sg.logger.debug('Reconciliating %s...' % obj)
            obj.reconciliate()
        return obj

    # Delete any object
    def delete(self, obj, given_session=None):
        sg.logger.debug('Deleting %s...' % obj)
        if given_session is None:
            session = self.new_session()
            obj = session.merge(obj)
            obj = session.delete(obj)
            session.commit()
            session.close()
        else:
            obj = given_session.delete(obj)
        return obj

    # Destructor
    def __del__(self):
        try:
            if self.session is not None:
                self.session.close()
            if self.engine is not None:
                self.engine.dispose()
        except Exception as e:
            pass
