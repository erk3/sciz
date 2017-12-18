#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import email, mailbox, ConfigParser, sys, os, traceback, datetime, re
from operator import itemgetter
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
        dir_path = self.mailDirPath + os.sep + group.mail.split('@')[0] + os.sep + 'parsed' + os.sep
        mail_max_retention = sg.config.get(sg.CONF_INSTANCE_SECTION, sg.CONF_INSTANCE_MAIL_RETENTION)
        now = datetime.datetime.now()
        ago = now - datetime.timedelta(minutes = int(mail_max_retention))
        try:
            for f in os.listdir(dir_path):
                last_modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(dir_path + os.sep + f))
                if last_modified_date < ago:
                    os.remove(dir_path + os.sep + f)
        except (OSError, IOError) as e:
            sg.logger.error('Fail to purge %s mail directory! (Error: %s)' % (dir_path, str(e), ))
            pass

    # Main MailDir walker
    def walk(self, group=None):
        group = group if group else sg.group
        try:
            # Open the mailbox
            sg.logger.info('Walking the mails for group %s...' % (group.flat_name, ))
            mbox = mailbox.Maildir(self.mailDirPath + os.sep + group.mail.split('@')[0])
            # Build a sorted list of key-message by 'Date' header #RFC822
            sorted_mbox = sorted(mbox.iteritems(), key=lambda x: email.utils.parsedate(x[1].get('Date')))
            # Then get the actuals mails
            actual_mails = map(lambda item : (mbox.get_file(item[0])._file.name, email.message_from_file(mbox.get_file(item[0]))), sorted_mbox)
            parsed_mails = map(lambda (file_name, mail) : (file_name, self.mp.parse_mail(mail)), actual_mails)
            # Then re-sort by MH date (if there is one), then by remaining PV (if indicated ; multiple mob attacks at the same second case)
            re_time = re.compile(sg.config.get(sg.CONF_SECTION_COMMON, sg.CONF_NOTIF_TIME))
            re_vie = re.compile(sg.config.get(sg.CONF_SECTION_BATTLE, sg.CONF_NOTIF_VIE))
            parsed_mails_with_attrs = map(lambda (n, (s, b)) : (n, s, b, re_time.search(b), re_vie.search(b)), parsed_mails)
            parsed_mails_with_attrs = map(lambda (n, s, b, t, v) : (n, s, b,
                datetime.datetime.strptime(t.groupdict()['time'], '%d/%m/%Y %H:%M:%S') if t else datetime.datetime.utcnow(),
                v.groupdict()['vie'] if v else None), parsed_mails_with_attrs)
            sorted_mails = sorted(parsed_mails_with_attrs, key=itemgetter(3, 4))
            # Finally walk over the mails
            for (file_name, subject, body, time, vie) in sorted_mails:
                try:
                    objs = self.mp.parse(subject, body, group)
                    if objs != None:
                        if not type(objs) is list: objs = [objs]
                        for obj in objs:
                            if not isinstance(obj, MAILHELPER):
                                obj = sg.db.add(obj)
                                sg.db.add_event(obj)

                    # Archive the mail
                    new_file = self.mailDirPath + os.sep + group.mail.split('@')[0] + os.sep + 'parsed' + os.sep + os.path.basename(file_name)
                    sg.createDirName(new_file)
                    os.rename(file_name, new_file)

                # If anything goes wrong parsing a mail, it will land here (hopefully) then continue
                except Exception:
                    sg.logger.warning('Fail to handle mail %s' % (file_name), exc_info=True)
                    print >> sys.stderr, 'Errors have been logged while handling mail %s' % (file_name)
                    pass

        except (OSError, IOError, mailbox.Error) as e:
            e.sciz_logger_flag = True
            sg.logger.error('Fail to scan mail directory! (Eerror: %s)' % (str(e), ))
            raise
