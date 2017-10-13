#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import email, mailbox, ConfigParser, sys, os, re, traceback
from operator import itemgetter
from email.header import decode_header
from modules.sql_helper import SQLHelper
from classes.cdm import CDM
from classes.battle_event import BATTLE_EVENT
from modules.pretty_printer import PrettyPrinter
import modules.globals as sg

## MailWalker class for SCIZ
class MailWalker:

    # Constructor
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.check_conf()
        self.sqlHelper = SQLHelper(config, logger)
    
    # Configuration loader and checker
    def check_conf(self):
        try:
            # Load Mail conf
            self.mailDirPath = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_PATH)
            self.mailRegexCDM = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_CDM_RE)
            self.mailRegexATT = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_ATT_RE)
            self.mailRegexDEF = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DEF_RE)
            self.mailRegexCAPA = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_CAPA_RE)
            self.mailRegexAttHYPNO = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_ATT_HYPNO_RE)
            self.mailRegexDefHYPNO = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DEF_HYPNO_RE)
            self.mailRegexAttSACRO = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_ATT_SACRO_RE)
            self.mailRegexDefSACRO = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DEF_SACRO_RE)
            self.mailRegexAttVT = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_ATT_VT_RE)
            self.mailRegexDefVT = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DEF_VT_RE)
            self.mailRegexAttEXPLO = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_ATT_EXPLO_RE)
            self.mailRegexDefEXPLO = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DEF_EXPLO_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            self.logger.error("Fail to load config! (ConfigParser error:" + str(e) + ")")
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



    # Main MailDir Walker
    def walk(self):
        try:
            mbox = mailbox.Maildir(self.mailDirPath)
            # Build a sorted list of key-message by 'Date' header #RFC822
            sorted_mails = sorted(mbox.iteritems(), key=lambda x: email.utils.parsedate(x[1].get('Date')))
            # Walk over the mail directory (iterating from the by 'Date' header sorted list)
            for mail in sorted_mails:
                msgFile = mbox.get_file(mail[0])
                msg = email.message_from_file(msgFile)
                self.__parse_mail(msg)
                try:
                    obj = None
                    # Handle CDM/ATT/DEF mails
                    if (re.search(self.mailRegexCDM, self.mail_subject) is not None):
                        self.logger.info('Found CDM in mail ' + msgFile._file.name)
                        obj = CDM()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, self.logger)
                    elif (re.search(self.mailRegexATT, self.mail_subject) is not None):
                        self.logger.info('Found ATT event in mail ' + msgFile._file.name)
                        obj = BATTLE_EVENT()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, self.logger, 'ATT')
                    elif (re.search(self.mailRegexDEF, self.mail_subject) is not None):
                        self.logger.info('Found DEF event in mail ' + msgFile._file.name)
                        obj = BATTLE_EVENT()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, self.logger, 'DEF')
                    elif (re.search(self.mailRegexDefHYPNO, self.mail_subject) is not None):
                        self.logger.info('Found DEF HYPNO event in mail ' + msgFile._file.name)
                        obj = BATTLE_EVENT()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, self.logger, 'DEF HYPNO')
                    elif (re.search(self.mailRegexAttHYPNO, self.mail_subject) is not None):
                        self.logger.info('Found ATT HYPNO event in mail ' + msgFile._file.name)
                        obj = BATTLE_EVENT()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, self.logger, 'ATT HYPNO')
                    elif (re.search(self.mailRegexDefSACRO, self.mail_subject) is not None):
                        self.logger.info('Found DEF SACRO event in mail ' + msgFile._file.name)
                        obj = BATTLE_EVENT()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, self.logger, 'DEF SACRO')
                    elif (re.search(self.mailRegexAttSACRO, self.mail_subject) is not None):
                        self.logger.info('Found ATT SACRO event in mail ' + msgFile._file.name)
                        obj = BATTLE_EVENT()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, self.logger, 'ATT SACRO')
                    elif (re.search(self.mailRegexDefVT, self.mail_subject) is not None):
                        self.logger.info('Found DEF VT event in mail ' + msgFile._file.name)
                        obj = BATTLE_EVENT()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, self.logger, 'DEF VT')
                    elif (re.search(self.mailRegexAttVT, self.mail_subject) is not None):
                        self.logger.info('Found ATT VT event in mail ' + msgFile._file.name)
                        obj = BATTLE_EVENT()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, self.logger, 'ATT VT')
                    elif (re.search(self.mailRegexDefEXPLO, self.mail_subject) is not None):
                        self.logger.info('Found DEF EXPLO event in mail ' + msgFile._file.name)
                        obj = BATTLE_EVENT()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, self.logger, 'DEF EXPLO')
                    elif (re.search(self.mailRegexAttEXPLO, self.mail_subject) is not None):
                        self.logger.info('Found ATT EXPLO event in mail ' + msgFile._file.name)
                        obj = BATTLE_EVENT()
                        obj = obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, self.logger, 'ATT EXPLO')
                    elif (re.search(self.mailRegexCAPA, self.mail_subject) is not None):
                        self.logger.info('Found CAPA event in mail ' + msgFile._file.name)
                        obj = BATTLE_EVENT()
                        obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, self.logger, 'DEF CAPA')
                    
                    if obj != None:
                        if not type(obj) is list: obj = [obj]
                        for obj in obj:
                            self.sqlHelper.add(obj)
                            self.sqlHelper.session.commit()
                            notif = self.sqlHelper.add_notif(obj)
                            self.sqlHelper.session.commit()
                            obj.notif_id = notif.id
                            self.sqlHelper.add(obj)
                            self.sqlHelper.session.commit()
                
                    os.remove(msgFile._file.name)
            
                # If anything goes wrong parsing a mail, it will land here (hopefully) then continue
                except Exception:
                    self.logger.warning('Fail to handle mail ' + msgFile._file.name, exc_info=True)
                    pass

        except OSError as e:
            e.sciz_logger_flag = True
            self.logger.error('Fail to scan mail directory! (I/O error: '+ str(e) + ')')
            raise
        
        except IOError as e:
            e.sciz_logger_flag = True
            self.logger.error('Fail to scan mail directory! (I/O error: '+ str(e) + ')')
            raise

        except mailbox.Error as e:
            e.sciz_logger_flag = True
            self.logger.error('Fail to scan mail directory! (MailBox error: ' + str(e) + ')')
            raise

