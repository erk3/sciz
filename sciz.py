#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import sys, argparse, ConfigParser, sqlalchemy, codecs, logging, os, traceback
from logging.handlers import RotatingFileHandler
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import ProgrammingError
from modules.mh_caller import MHCaller
from modules.mail_walker import MailWalker
from modules.admin_helper import AdminHelper
from modules.notifier import Notifier
from modules.requester import Requester
from modules.sql_helper import SQLHelper
from modules.game_engine import GameEngine
from classes.conf import CONF
from classes.group import GROUP
import modules.globals as sg

# Ignore SIGPIPE, not sure this is a good idea but it fixes the random broken pipe problem
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL) 

## SCIZ
class SCIZ:

    # Constructor
    def __init__(self, conf_file, logging_level, group):

        # Load the default conf and store it globally
        sg.config = ConfigParser.RawConfigParser()
        with codecs.open(conf_file, 'r', sg.DEFAULT_CHARSET) as fp:
            sg.config.readfp(fp)
        
        # Set up the logger and store it globally
        logger_file = sg.config.get(sg.CONF_LOG_SECTION, sg.CONF_LOG_FILE)
        logger_file_max_size = sg.config.getint(sg.CONF_LOG_SECTION, sg.CONF_LOG_FILE_MAX_SIZE)
        logger_formatter = sg.config.get(sg.CONF_LOG_SECTION, sg.CONF_LOG_FORMATTER)
        sg.createDirName(logger_file);
        log_file = RotatingFileHandler(logger_file, 'a', logger_file_max_size, 1)
        log_file.setLevel(logging_level)
        log_file.setFormatter(logging.Formatter(logger_formatter))
        sg.logger = logging.getLogger()
        sg.logger.setLevel(logging.DEBUG)
        sg.logger.addHandler(log_file)
        
        # Set up the database connection and store it globally
        sg.db =  SQLHelper()
        
        # Load the stored configuration
        try:
            confs = sg.db.session.query(CONF).filter(CONF.group_id == None, CONF.section == sg.CONF_INSTANCE_SECTION).all()
            for conf in confs:
                sg.config.set(sg.CONF_INSTANCE_SECTION, conf.key, conf.value)
            sg.logger.info('Loaded stored configurations for the instance!')
        except Exception as e:
            sg.logger.warning('No configurations found for the instance!')

        # Set up the Game Engine
        sg.ge = GameEngine()

    # Mail walker 
    def walk(self):
        self.walker = MailWalker()
        self.adminHelper = AdminHelper()
        if sg.group:
            # A group is already set, its conf has already been loaded
            self.walker.walk(sg.group)
        else:
            groups = sg.db.session.query(GROUP).all()
            for group in groups:
                # Ensure to load the conf for the group
                self.adminHelper.set_group(group.flat_name)
                # Then walk the mails
                self.walker.walk(group)
    
    # Notifier
    def notify(self, hook_name):
        self.notifier = Notifier()
        self.notifier.print_flush(hook_name)

    # Requester
    def request(self, ids, args):
        self.requester = Requester()
        if ids.lower() == 'help':
            print 'syntax: id_mob[,id_mob]* [opts_mob] | (id_troll[,id_troll]*|trolls|users) [opts_troll] | help'
            print 'opts_mob : '' #default=all caracs# | (cdm|event|recap) [limit=1] | carac[,carac]* #ordered desc by first carac#'
            print 'opts_troll : '' #default=all caracs# | (aa|event) [limit=1] | carac[,carac] | update* #ordered desc by first carac#'
        else:
            self.requester.request(ids, args)
            
    # Mountyhall caller
    def mh_call(self, script, trolls):
        self.mhCaller = MHCaller()
        self.mhCaller.call(script, trolls)
            
    # Admin helper
    def admin(self, cmd, arg=None):
        self.adminHelper = AdminHelper()
        if cmd == 'init':
            self.adminHelper.init()
        elif cmd == 'auto':
            self.adminHelper.auto_tasks()
        elif cmd == 'group':
            self.adminHelper.set_group(arg)
        elif cmd == 'reset-confs':
            self.adminHelper.reset_groups_conf(arg)
    
    # Destructor
    def __del__(self):
        pass

## MAIN

if __name__ == '__main__':
    
    # Command line arguments handling
    parser = argparse.ArgumentParser(
            description='Système de Chauve-souris Interdimensionnel pour Zhumains',
            epilog='From Põm³ with love')
    
    parser.add_argument('-c', '--conf',
            metavar='CONFIG_FILE', type=str, default='confs/sciz.ini',
            help='specify the .ini configuration file')
    
    parser.add_argument('-l', '--logging-level',
            metavar='LOGGING_LEVEL', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
            help='specify the level of logging')
    
    parser.add_argument('-a', '--auto',
            action='store_true',
            help='instruct SCIZ to start the recurrent automagic things')
    
    parser.add_argument('-r', '--request',
            metavar='REQUEST_CLI | help', type=str,
            help='instruct SCIZ to pull internal data')
    
    parser.add_argument('-w', '--walk',
            action='store_true',
            help='instruct SCIZ to walk the mails')
    
    parser.add_argument('-n', '--notify',
            metavar='HOOK_NAME', type=str,
            help='instruct SCIZ to push the pending notifications for a hook')
    
    parser.add_argument('-s', '--script',
            metavar='PUBLIC_SCRIPT [troll]', choices=['profil4', 'trolls2', 'monstres', 'tresors', 'capas', 'vue2'],
            help='instruct SCIZ to call a MountyHall Public Script / FTP')

    parser.add_argument('-i', '--init',
            action='store_true',
            help='instruct SCIZ to setup the things')
    
    parser.add_argument('-z', '--reset-confs',
            metavar='GROUP_NAME', type=str, nargs='?', const=True, default=None,
            help='instruct SCIZ to reset the confs for all groups')
    
    parser.add_argument('-g', '--group',
            metavar='GROUP_NAME', type=str,
            help='set the working group')
   
    parser.add_argument('rargs', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.request and not args.group:
        parser.error('option `-r --request` requires option `-g --group`')
    if args.notify and not args.group:
        parser.error('option `-n --notify` requires option `-g --group`')
    if args.walk and not args.group:
        parser.error('option `-w --walk` requires option `-g --group`')
    
    # SCIZ startup
    sciz = None
    print_help = False
    try:
        sciz = SCIZ(args.conf, args.logging_level, args.group)
        sg.logger.info('SCIZ woke up successfully!')
        if args.group and not args.auto and not args.init and not args.script and not args.reset_confs:
            sciz.admin('group', args.group)
        else:
            sg.group = None
        if args.init:
            sg.logger.info('Initializing DB...')
            sciz.admin('init', args.init)
        elif args.reset_confs:
            sciz.admin('reset-confs', args.reset_confs)
        elif args.auto:
            sg.logger.info('Starting recurrent tasks...')
            sciz.admin('auto')
        elif args.script:
            sg.logger.info('Calling MountyHall...')
            sciz.mh_call(args.script, args.rargs)
        elif args.walk:
            sg.logger.info('Walking the mails...')
            sciz.walk()
        elif args.notify:
            sg.logger.info('Notifying for hook %s...' % (args.notify, ))
            sciz.notify(args.notify)
        elif args.request:
            sg.logger.info('Requesting SCIZ...')
            sciz.request(args.request, args.rargs)
        else:
            parser.print_help()
        sg.logger.info('Nothing else to do, going to sleep now.')
    except Exception as e:
        if sciz and sg.logger and not hasattr(e, 'sciz_logger_flag'):
            sg.logger.exception(e)
        else:
            traceback.print_exc()
        print >> sys.stderr, 'Aborted. Check the log file, if no new line has been appended, either your logging level is unsufficient or an error occured before basically everything.'
        sys.exit(1)
