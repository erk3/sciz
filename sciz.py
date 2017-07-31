#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import sys, argparse, ConfigParser, sqlalchemy, json, codecs
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
    def __init__(self, confFile):
        # Load the conf
        self.confFile = confFile
        self.reload()
    
    # Configuration loaders
    def reload(self):
        self.load(self.confFile)

    def load(self, confFile):
        self.config = ConfigParser.ConfigParser()
        try:
            with codecs.open(self.confFile, 'r', sg.DEFAULT_CHARSET) as fp:
                self.config.readfp(fp)
        except IOError as e:
            print('Fail to load config file! (I/O error:' + str(e) + ')')
            raise

    # Mail walker 
    def walk(self):
        self.walker = MailWalker(self.config)
        self.walker.walk()

    # SCIZ Notifier
    def notify(self):
        # FIXME : maybe later, handle other push vectors like pushover or whatever not on the stdout
        self.notifier = Notifier(self.config)
        self.notifier.print_all()
        self.notifier.flush()

    # SCIZ Requester
    def request(self, entity, args):
        self.requester = Requester(self.config)
        if not args and entity == 'mob':
            print 'syntax: mob [mob_ids, caracs/*] [mob_ids, last_cdm] [mob_ids, last_event limit]'
        elif not args and entity == 'troll':
            print 'syntax: troll [troll_ids,/* caracs/*] [troll_ids,/* last_event limit] [troll_ids,/* dla] [troll_ids,/* pos]'
        else:
            self.requester.request(entity, args)
            
    # Mountyhall caller
    def mh_call(self, script, trolls):
        self.mhCaller = MHCaller(self.config)
        self.mhCaller.call(script, trolls)
            
    # Admin helper
    def admin(self, cmd, arg=None):
        self.adminHelper = AdminHelper(self.config)
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
    parser.add_argument('-t', '--test', action='store_true', help='instruct SCIZ to test your thing')
    parser.add_argument('-u', '--users', metavar = 'USERS_FILE', type=str, help='instruct SCIZ to create or update users from JSON')
    parser.add_argument('-i', '--init', action='store_true', help='instruct SCIZ to setup the things')
    parser.add_argument('-s', '--script', metavar='PUBLIC_SCRIPT [troll]', choices=['profil2', 'caract', 'trolls2', 'monstres'], help='instruct SCIZ to call a MountyHall Public Script / FTP')
    parser.add_argument('-r', '--request', metavar='mob/troll ...', choices=['mob', 'troll', 'dla'], help='instruct SCIZ to pull internal data')
    parser.add_argument('-w', '--walk', action='store_true', help='instruct SCIZ to walk the mails')
    parser.add_argument('-n', '--notify', action='store_true', help='instruct SCIZ to push the pending notifications')
    parser.add_argument('rargs', nargs=argparse.REMAINDER, help=argparse.SUPPRESS)
    args = parser.parse_args()
    
    # SCIZ startup
    #try:
    sciz = SCIZ(args.conf)
    if args.init:
        # FIXME: mode verbose / logger
        #print 'Initializing DB...'
        sciz.admin('init')
    elif args.users:
        # FIXME: mode verbose / logger
        #print 'Updating users...'
        sciz.admin('users', args.users)
    elif args.walk:
        # FIXME: mode verbose / logger
        #print 'Walking the mails...'
        sciz.walk()
    elif args.script:
        # FIXME: mode verbose / logger
        #print 'Calling MountyHall...'
        sciz.mh_call(args.script, args.rargs)
    elif args.notify:
        # FIXME: mode verbose / logger
        #print 'Calling notifier...'
        sciz.notify()
    elif args.request:
        # FIXME: mode verbose / logger
        #print 'Requesting SCIZ...'
        sciz.request(args.request, args.rargs)
    elif args.test:
        # FIXME: mode verbose / logger
        #print 'Testing something...'
        sciz.test()
    # FIXME: mode verbose / logger
    #print 'Nothing else to do, going to sleep now.'
    #except:
    #    print 'Aborted.'
    #    sys.exit(1)
