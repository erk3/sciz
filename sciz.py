#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import sys, argparse, ConfigParser, sqlalchemy, json, codecs, logging, os
from logging.handlers import RotatingFileHandler
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from modules.mh_caller import MHCaller
from modules.mail_walker import MailWalker
from modules.admin_helper import AdminHelper
from modules.notifier import Notifier
from modules.requester import Requester
import modules.globals as sg

## SCIZ

class SCIZ:

    # Constructor
    def __init__(self, confFile, loggingLevel):
        # Load the conf
        self.confFile = confFile
        self.reload()
        # Set the logger
        if not os.path.exists(os.path.dirname(self.logger_file)):
            try:
                os.makedirs(os.path.dirname(self.logger_file))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        log_file = RotatingFileHandler(self.logger_file, 'a', self.logger_file_max_size, 1)
        log_file.setLevel(loggingLevel)
        log_file.setFormatter(logging.Formatter(self.logger_formatter))
        self.logger.addHandler(log_file)
    
    # Configuration loaders
    def reload(self):
        self.load(self.confFile)

    def load(self, confFile):
        self.config = ConfigParser.RawConfigParser()
        try:
            with codecs.open(self.confFile, 'r', sg.DEFAULT_CHARSET) as fp:
                self.config.readfp(fp)
            self.logger_file = self.config.get(sg.CONF_LOG_SECTION, sg.CONF_LOG_FILE)
            self.logger_file_max_size = self.config.get(sg.CONF_LOG_SECTION, sg.CONF_LOG_FILE_MAX_SIZE)
            self.logger_formatter = self.config.get(sg.CONF_LOG_SECTION, sg.CONF_LOG_FORMATTER)
        except Exception as e:
            print >> sys.stderr, 'Fail to load minimal config file or its minmal log section! (' + str(e) + ')'
            sys.exit(1)

    # Mail walker 
    def walk(self):
        self.walker = MailWalker(self.config, self.logger)
        self.walker.walk()

    # SCIZ Notifier
    def notify(self):
        # FIXME : maybe later, handle other push vectors like pushover or whatever not on the stdout
        self.notifier = Notifier(self.config, self.logger)
        self.notifier.print_all()
        self.notifier.flush()

    # SCIZ Requester
    def request(self, ids, args):
        self.requester = Requester(self.config, self.logger)
        if ids.lower() == 'help':
            print 'syntax: id_mob[,id_mob]* [opts_mob] | (id_troll[,id_troll]*|trolls) [opts_troll] | help'
            print 'opts_mob : stats #default# | (cdm|event) [limit=1] | carac[,carac]* #ordered desc by first carac#'
            print 'opts_troll : stats #default# | event [limit=1] | carac[,carac]* #ordered desc by first carac#'
        else:
            self.requester.request(ids, args)
            
    # Mountyhall caller
    def mh_call(self, script, trolls):
        self.mhCaller = MHCaller(self.config, self.logger)
        self.mhCaller.call(script, trolls)
            
    # Admin helper
    def admin(self, cmd, arg=None):
        self.adminHelper = AdminHelper(self.config, self.logger)
        if cmd == 'init':
            self.adminHelper.init()
        elif cmd == 'users':
            self.adminHelper.update_users(arg)
    
    # Tester (WRITE ANY TEST HERE)
    def test(self):
        pass

    # Destructor
    def __del__(self):
        pass

## MAIN

if __name__ == '__main__':
    
    # Command line arguments handling
    parser = argparse.ArgumentParser(
             description='Système de Chauve-souris Interdimensionnel pour Zhumains',
             epilog='From Põm³ with love')
    parser.add_argument('-c', '--conf', metavar='CONFIG_FILE', type=str, default='confs/sciz.ini', help='specify the .ini configuration file')
    parser.add_argument('-l', '--logging-level', metavar='LOGGING_LEVEL', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='specify the level of logging')
    parser.add_argument('-t', '--test', action='store_true', help='instruct SCIZ to test your thing')
    parser.add_argument('-u', '--users', metavar = 'USERS_FILE', type=str, help='instruct SCIZ to create or update users from JSON')
    parser.add_argument('-i', '--init', action='store_true', help='instruct SCIZ to setup the things')
    parser.add_argument('-s', '--script', metavar='PUBLIC_SCRIPT [troll]', choices=['profil2', 'caract', 'trolls2', 'monstres'], help='instruct SCIZ to call a MountyHall Public Script / FTP')
    parser.add_argument('-r', '--request', metavar='REQUEST_CLI | help', type=str, help='instruct SCIZ to pull internal data')
    parser.add_argument('-w', '--walk', action='store_true', help='instruct SCIZ to walk the mails')
    parser.add_argument('-n', '--notify', action='store_true', help='instruct SCIZ to push the pending notifications')
    parser.add_argument('rargs', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    args = parser.parse_args()
    
    # SCIZ startup
    try:
        sciz = SCIZ(args.conf, args.logging_level)
        sciz.logger.info('SCIZ woke up successfully!')
        if args.init:
            sciz.logger.info('Initializing DB...')
            sciz.admin('init')
        elif args.users:
            sciz.logger.info('Updating users...')
            sciz.admin('users', args.users)
        elif args.walk:
            sciz.logger.info('Walking the mails...')
            sciz.walk()
        elif args.script:
            sciz.logger.info('Calling MountyHall...')
            sciz.mh_call(args.script, args.rargs)
        elif args.notify:
            sciz.logger.info('Calling notifier...')
            sciz.notify()
        elif args.request:
            sciz.logger.info('Requesting SCIZ...')
            sciz.request(args.request, args.rargs)
        elif args.test:
            sciz.logger.info('Testing something...')
            sciz.test()
        sciz.logger.info('Nothing else to do, going to sleep now.')
    except Exception as e:
        if not hasattr(e, 'sciz_logger_flag'):
            sciz.logger.exception(e)
        print >> sys.stderr, 'Aborted. Check the log file, if no new line has been appended, either your logging level is unsufficient or an error occured before basically everything'
        sys.exit(1)
