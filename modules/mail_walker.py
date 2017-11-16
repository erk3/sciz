#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import email, mailbox, ConfigParser, sys, os, re, traceback, datetime
from operator import itemgetter
from email.header import decode_header
from modules.sql_helper import SQLHelper
from classes.cdm import CDM
from classes.battle import BATTLE
from classes.piege import PIEGE
from classes.group import GROUP
from classes.event import EVENT
from modules.pretty_printer import PrettyPrinter
import modules.globals as sg

## MailWalker class for SCIZ
class MailWalker:

    # Constructor
    def __init__(self):
        self.check_conf()
        
    # Configuration loader and checker
    def check_conf(self):
        try:
            # Load Mail conf
            self.mailDirPath = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_PATH)
            self.mailRegexCDM = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_CDM_RE)
            self.mailRegexATT = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_ATT_RE)
            self.mailRegexDEF = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DEF_RE)
            self.mailRegexCAPA = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_CAPA_RE)
            self.mailRegexPIEGE = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_PIEGE_RE)
            self.mailRegexAttHYPNO = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_ATT_HYPNO_RE)
            self.mailRegexDefHYPNO = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DEF_HYPNO_RE)
            self.mailRegexAttSACRO = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_ATT_SACRO_RE)
            self.mailRegexDefSACRO = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DEF_SACRO_RE)
            self.mailRegexAttVT = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_ATT_VT_RE)
            self.mailRegexDefVT = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DEF_VT_RE)
            self.mailRegexAttEXPLO = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_ATT_EXPLO_RE)
            self.mailRegexDefEXPLO = sg.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DEF_EXPLO_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error:" + str(e) + ")")
            raise

    # Utility mail parser
    def __parse_mail(self, msg):
        # Subject
        subject = decode_header(msg['subject'])[0][0]
        if msg.get_content_charset():
            subject = subject.decode(msg.get_content_charset())
            subject = subject.encode(sg.DEFAULT_CHARSET)
        self.mail_subject = subject.decode(sg.DEFAULT_CHARSET)
        # Body
        body = ''
        if msg.is_multipart():
            for part in msg.walk():
                payload = part.get_payload(decode=True)
                if part.get_content_charset():
                    payload = payload.decode(part.get_content_charset())
                    payload = payload.encode(sg.DEFAULT_CHARSET)
                if payload:
                    body += payload
        else:
            body = msg.get_payload(decode=True)
            if msg.get_content_charset():
                body = body.decode(msg.get_content_charset())
                body = body.encode(sg.DEFAULT_CHARSET)
        self.mail_body = body.decode(sg.DEFAULT_CHARSET)

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
            sg.logger.error('Fail to purge %s mail directory! (I/O error: %s)' % (group.flat_name, str(e), ))
            pass

    # Main MailDir Walker
    def walk(self, group=None):
        group = group if group else sg.group
        try:
            sg.logger.info('Walking the mails for group %s...' % (group.flat_name, ))
            mbox = mailbox.Maildir(self.mailDirPath + os.sep + group.flat_name)
            # Build a sorted list of key-message by 'Date' header #RFC822
            sorted_mails = sorted(mbox.iteritems(), key=lambda x: email.utils.parsedate(x[1].get('Date')))
            # Walk over the mail directory (iterating from the by 'Date' header sorted list)
            for mail in sorted_mails:
                msgFile = mbox.get_file(mail[0])
                msg = email.message_from_file(msgFile)
                self.__parse_mail(msg)
                try:
                    obj = None
                    # Handle mails
                    if (re.search(self.mailRegexCDM, self.mail_subject) is not None):
                        sg.logger.info('Found CDM in mail %s' % (msgFile._file.name, ))
                        obj = CDM()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, group)
                    elif (re.search(self.mailRegexATT, self.mail_subject) is not None):
                        sg.logger.info('Found ATT event in mail %s' % (msgFile._file.name, ))
                        obj = BATTLE()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, group, 'ATT')
                    elif (re.search(self.mailRegexDEF, self.mail_subject) is not None):
                        sg.logger.info('Found DEF event in mail %s' % (msgFile._file.name, ))
                        obj = BATTLE()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, group, 'DEF')
                    elif (re.search(self.mailRegexDefHYPNO, self.mail_subject) is not None):
                        sg.logger.info('Found DEF HYPNO event in mail %s' % (msgFile._file.name, ))
                        obj = BATTLE()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, group, 'DEF HYPNO')
                    elif (re.search(self.mailRegexAttHYPNO, self.mail_subject) is not None):
                        sg.logger.info('Found ATT HYPNO event in mail %s' % (msgFile._file.name, ))
                        obj = BATTLE()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, group, 'ATT HYPNO')
                    elif (re.search(self.mailRegexDefSACRO, self.mail_subject) is not None):
                        sg.logger.info('Found DEF SACRO event in mail %s' % (msgFile._file.name, ))
                        obj = BATTLE()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, group, 'DEF SACRO')
                    elif (re.search(self.mailRegexAttSACRO, self.mail_subject) is not None):
                        sg.logger.info('Found ATT SACRO event in mail %s' % (msgFile._file.name, ))
                        obj = BATTLE()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, group, 'ATT SACRO')
                    elif (re.search(self.mailRegexDefVT, self.mail_subject) is not None):
                        sg.logger.info('Found DEF VT event in mail %s' % (msgFile._file.name, ))
                        obj = BATTLE()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, group, 'DEF VT')
                    elif (re.search(self.mailRegexAttVT, self.mail_subject) is not None):
                        sg.logger.info('Found ATT VT event in mail %s' % (msgFile._file.name, ))
                        obj = BATTLE()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, group, 'ATT VT')
                    elif (re.search(self.mailRegexDefEXPLO, self.mail_subject) is not None):
                        sg.logger.info('Found DEF EXPLO event in mail %s' % (msgFile._file.name, ))
                        obj = BATTLE()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, group, 'DEF EXPLO')
                    elif (re.search(self.mailRegexAttEXPLO, self.mail_subject) is not None):
                        sg.logger.info('Found ATT EXPLO event in mail %s' % (msgFile._file.name, ))
                        obj = BATTLE()
                        obj = obj.populate_from_mail(self.mail_subject, self.mail_body, group, 'ATT EXPLO')
                    elif (re.search(self.mailRegexCAPA, self.mail_subject) is not None):
                        sg.logger.info('Found CAPA event in mail %s' % (msgFile._file.name, ))
                        obj = BATTLE()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, group, 'DEF CAPA')
                    elif (re.search(self.mailRegexPIEGE, self.mail_subject) is not None):
                        sg.logger.info('Found PIEGE event in mail %s' % (msgFile._file.name, ))
                        obj = PIEGE()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, group)
                    
                    if obj != None:
                        if not type(obj) is list: obj = [obj]
                        for obj in obj:
                            sg.db.add(obj)
                            event = EVENT()
                            sg.db.add(event, obj)
                    
                    new_file = self.mailDirPath + os.sep + group.flat_name + os.sep + 'parsed' + os.sep + os.path.basename(msgFile._file.name)
                    sg.createDirName(new_file)
                    os.rename(msgFile._file.name, new_file)

                # If anything goes wrong parsing a mail, it will land here (hopefully) then continue
                except Exception:
                    sg.logger.warning('Fail to handle mail %s' % (msgFile._file.name, ), exc_info=True)
                    print >> sys.stderr, 'Errors have been logged while handling mail %s' % (msgFile._file.name, )
                    pass

        except (OSError, IOError) as e:
            e.sciz_logger_flag = True
            sg.logger.error('Fail to scan mail directory! (I/O error: %s)' % (str(e), ))
            raise
        
        except mailbox.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error('Fail to scan mail directory! (MailBox error: %s)' % (str(e), ))
            raise

