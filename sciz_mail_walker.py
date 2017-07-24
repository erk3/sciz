#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import email, mailbox, ConfigParser, sys, os, re
from email.header import decode_header
from sciz_sql_helper import SQLHelper
from sciz_cdm_class import CDM
from sciz_battle_event_class import BATTLE_EVENT
from sciz_pretty_printer import PrettyPrinter
import sciz_globals as sg

## MailWalker class for SCIZ
class MailWalker:

    # Constructor
    def __init__(self, config):
        self.config = config
        self.check_conf()
        self.sqlHelper = SQLHelper(config)
    
    # Configuration loader and checker
    def check_conf(self):
        try:
            # Load Mail conf
            self.mailDirPath = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_PATH)
            self.mailRegexCDM = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_CDM_RE)
            self.mailRegexATT = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_ATT_RE)
            self.mailRegexDEF = self.config.get(sg.CONF_MAIL_SECTION, sg.CONF_MAIL_DEF_RE)
        except ConfigParser.Error as e:
            print("Fail to load config! (ConfigParser error:" + str(e) + ")")
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
            
            # Walk over the mail directory
            for key in mbox.keys():
                msgFile = mbox.get_file(key)
                msg = email.message_from_file(msgFile)
                self.__parse_mail(msg)

                obj = None
                # Handle CDM/ATT/DEF mails
                if (re.search(self.mailRegexCDM, self.mail_subject) is not None):
                    # FIXME: mode verbose / logger
                    #print 'Found CDM in mail ' + msgFile._file.name
                    obj = CDM()
                    obj.populate_from_mail(self.mail_subject, self.mail_body, self.config)
                elif (re.search(self.mailRegexATT, self.mail_subject) is not None):
                    # FIXME: mode verbose / logger
                    #print 'Found ATT event in mail ' + msgFile._file.name
                    obj = BATTLE_EVENT()
                    obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, 'ATT')
                elif (re.search(self.mailRegexDEF, self.mail_subject) is not None):
                    # FIXME: mode verbose / logger
                    #print 'Found DEF event in mail ' + msgFile._file.name
                    obj = BATTLE_EVENT()
                    obj.populate_from_mail(self.mail_subject, self.mail_body, self.config, 'DEF')
                
                if obj != None:
                    self.sqlHelper.add(obj)
                    self.sqlHelper.session.commit()
                    notif = self.sqlHelper.add_notif(obj)
                    self.sqlHelper.session.commit()
                    obj.notif_id = notif.id
                    self.sqlHelper.add(obj)
                    self.sqlHelper.session.commit()
                
                os.remove(msgFile._file.name)

        except OSError as e:
            print 'Fail to scan mail directory! (I/O error: '+ str(e) + ')'
            raise
        
        except IOError as e:
            print 'Fail to scan mail directory! (I/O error: '+ str(e) + ')'
            raise

        except mailbox.Error as e:
            print 'Fail to scan mail directory! (MailBox error: ' + str(e) + ')'
            raise

