#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import re, ConfigParser, email, HTMLParser
from classes.cdm import CDM
from classes.piege import PIEGE
from classes.battle import BATTLE
from classes.portal import PORTAL
from modules.mail_helper import MAILHELPER
import modules.globals as sg

## MailParser class for SCIZ
class MailParser:

    # Constructor
    def __init__(self):
        pass

    # Utility mail parser
    def parse_mail(self, msg):
        mail_subject = None
        mail_body = None
        try:
            tuple_subject_charset = email.header.decode_header(msg['subject'])
            subject = tuple_subject_charset[0][0]
            charset = tuple_subject_charset[0][1]
            # Use the embedded charset in the subject if any
            if charset:
                charset = 'mac-roman' if (charset == 'macintosh') else charset # Dirty hack for really old Apple mail clients (< OS X)
                subject = subject.decode(charset)
            # Else use any global charset for the mail
            elif msg.get_content_charset():
                subject = subject.decode(msg.get_content_charset())
            # Else assume it is utf-8
            else:
                subject = subject.encode(sg.DEFAULT_CHARSET)
            mail_subject = subject
            # Body
            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        payload = part.get_payload(decode=True)
                        if payload is not None and part.get_content_charset():
                            body += payload.decode(part.get_content_charset())
                        elif payload is not None:
                            body += payload.decode(sg.DEFAULT_CHARSET)
            else:
                body = msg.get_payload(decode=True)
                if msg.get_content_charset():
                    body = body.decode(msg.get_content_charset())
                else:
                    body = body.decode(sg.DEFAULT_CHARSET)
            mail_body = body
        except Exception as e:
            sg.logger.error('Failed to parse a mail: %s' % (str(e)))
        # Just in case some htmlentities were put in the mail...
        h = HTMLParser.HTMLParser()
        mail_body = h.unescape(mail_body)
        # Result
        return (mail_subject, mail_body)

    # Utility regexps loader from sections of the .ini file
    def __load_regexps_section(self, sections):
        try:
            res = []
            for section in sections:
                section = section.lower()
                if sg.config.has_section(section):
                    res = sum([res, map(lambda (k, v): (k, re.compile(v)), sg.config.items(section))], [])
            return res
        except (re.error, ConfigParser.Error) as e:
            e.sciz_logger_flag = True
            sg.logger.error('Failed to load regexp! Error: %s)' % (str(e), ))
            raise
    
    def __match_first_regexp(self, regexps, payload):
        for (k, r) in regexps:
            match = r.search(payload)
            if match is not None:
                return (k, match.groupdict())
        return (None, None)
    
    # Main regexp dispatcher and CLASS.populate dispatcher
    def parse(self, subject, body, group):
        if subject is None or body is None:
            return None
        # Dictionary of dictionaries with the results of the regexp matching
        # The first item has all the regexps matching at least one time
        # The following items are for occurences of regexps matching several times
        # At the end all the regexps of the first item not in the others are copied
        res = {0: {}}
        # Loop over the regexp for ignored subject matching
        ignored_regexps = self.__load_regexps_section([sg.CONF_SECTION_IGNORED_SUBJECTS])
        (key, res[0]) = self.__match_first_regexp(ignored_regexps, subject)
        if key is not None: 
            sg.logger.warning('Ignored mail, aborting...')
            return None
        # Loop over the regexp for subject matching
        regexps = self.__load_regexps_section([sg.CONF_SECTION_SUBJECTS])
        (key, res[0]) = self.__match_first_regexp(regexps, subject)
        if key is None:
            sg.logger.warning('No regexp matching mail subject \'%s\', aborting...' % (subject))
            return None
        sg.logger.info('Found \'%s\' in the mail subject' % (key))
        # Routine is called based on key, which must be 'CLASS(_\w+)?'
        # formated, for CLASS.build or CLASS.build_\1 to be called.
        # This is probably dangerous behavior but since no people should be
        # allowed to access the .ini config file without having also access to
        # this piece of code, this seems a nice code/logic factoring feature.
        split = key.split('_', 1)
        _class = split[0].upper()
        _method = 'build' if len(split) == 1 else 'build_' + split[1].lower()
        # The .ini config file must also have a section named as the
        # key that previously matched or at least the class name with all the
        # associated regexps to match in the mail
        regexps = self.__load_regexps_section([sg.CONF_SECTION_COMMON, _class, key])
        matchs = map(lambda (k, r): (k, r.finditer(body)), regexps)
        for (key, matchall) in matchs:
            i = 0
            for match in matchall:
                if match is not None:
                    if not res.has_key(i):
                        res[i] = {}
                    res[i].update(match.groupdict())
                i += 1
        # Update all the events with the first one
        if len(res) > 1:
            for (key, value) in res[0].items():
                for (i, values) in res.items():
                    if i > 0 and not values.has_key(key):
                        res[i].update({key: value})
        # Finally, create and populate the object (CDM, BATTLE, PIEGE...)
        # usging the dictionary of named group that matched
        objs = []
        for value_set in res.values():
            try:
                obj = globals()[_class]()
            except KeyError as e:
                sg.logger.error('No class \'%s\' imported for an allowed parsing, aborting...' % (_class))
                return None
            obj.group_mail = group.mail
            obj.group_id = group.id
            for key in value_set:
                setattr(obj, key, value_set[key])
            # Also do any additionnal logic related (.build methods)
            if hasattr(globals()[_class], _method) and callable(getattr(globals()[_class], _method)):
                getattr(obj, _method)()
            else:
                sg.logger.warning('No build routine in class \'%s\' for additional logic' % (_class))
            objs.append(obj)
        return objs
    
