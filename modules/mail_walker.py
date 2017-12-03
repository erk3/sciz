#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import email, mailbox, ConfigParser, sys, os, traceback, datetime
from modules.mail_parser import MailParser
from modules.mail_helper import MAILHELPER
from classes.event import EVENT
import modules.globals as sg

## MailWalker class for SCIZ
class MailWalker:

    # Constructor
    def __init__(self):
        self.mp = MailParser()
        self.check_conf()
        
    # Configuration loader and checker
    def check_conf(self):
        try:
            self.mailDirPath = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_PATH)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error:" + str(e) + ")")
            raise

    # Purge routine
    def purge(self, group=None):
        group = group if group else sg.group
        dir_path = self.mailDirPath + os.sep + group.flat_name + os.sep + 'parsed' + os.sep
        mail_max_retention = sg.config.get(sg.CONF_INSTANCE_SECTION, sg.CONF_INSTANCE_MAIL_RETENTION)
        now = datetime.datetime.now()
        ago = now - datetime.timedelta(minutes = int(mail_max_retention))
        try:
            for f in os.listdir(dir_path):
                last_modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(dir_path + os.sep + f))
                if last_modified_date < ago:
                    os.remove(dir_path + os.sep + f)
        except (OSError, IOError) as e:
            sg.logger.error('Fail to purge %s mail directory! (Error: %s)' % (group.flat_name, str(e), ))
            pass

    # Main MailDir walker
    def walk(self, group=None):
        group = group if group else sg.group
        try:
            # Open the mailbox
            sg.logger.info('Walking the mails for group %s...' % (group.flat_name, ))
            mbox = mailbox.Maildir(self.mailDirPath + os.sep + group.mail.split('@')[0])
            
            # Build a sorted list of key-message by 'Date' header #RFC822
            sorted_mails = sorted(mbox.iteritems(), key=lambda x: email.utils.parsedate(x[1].get('Date')))
            
            # Walk over the mail directory
            for mail in sorted_mails:
                mailFile = mbox.get_file(mail[0])
                mail = email.message_from_file(mailFile)
                try:
                    objs = self.mp.parse(mail, group)
                    
                    if objs != None:
                        if not type(objs) is list: objs = [objs]
                        for obj in objs:
                            if not isinstance(obj, MAILHELPER):
                                sg.db.add(obj)
                                sg.db.add_event(obj)

                    # Archive the mail
                    new_file = self.mailDirPath + os.sep + group.mail.split('@')[0] + os.sep + 'parsed' + os.sep + os.path.basename(mailFile._file.name)
                    sg.createDirName(new_file)
                    os.rename(mailFile._file.name, new_file)

                # If anything goes wrong parsing a mail, it will land here (hopefully) then continue
                except Exception:
                    sg.logger.warning('Fail to handle mail %s' % (mailFile._file.name, ), exc_info=True)
                    print >> sys.stderr, 'Errors have been logged while handling mail %s' % (mailFile._file.name, )
                    pass

        except (OSError, IOError, mailbox.Error) as e:
            e.sciz_logger_flag = True
            sg.logger.error('Fail to scan mail directory! (Eerror: %s)' % (str(e), ))
            raise
