#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.event_aa import aaEvent
from classes.event_cdm import cdmEvent
from classes.event_tp import tpEvent
from classes.event_cp import cpEvent
from classes.event_champi import champiEvent
from classes.event_tresor import tresorEvent
from classes.event_battle import battleEvent
from modules.mail_helper import MailHelper
import re, email, html.parser
import modules.globals as sg


# CLASS DEFINITION
class MailParser:

    # Constructor
    def __init__(self):
        pass

    # Utility mail parser
    def parse_mail(self, msg):
        mail_subject = None
        mail_body = None
        mail_froms = []
        try:
            # From
            tuples_from_charset = email.header.decode_header(msg['from'])
            for tuple in tuples_from_charset:
                _from = tuple[0]
                charset = tuple[1]
                if isinstance(_from, bytes):
                    if charset is not None:
                        charset = 'mac-roman' if (charset == 'macintosh') else charset  # Dirty hack for really old Apple mail clients (< OS X)
                        _from = _from.decode(charset)
                    # Else use any global charset for the mail
                    elif msg.get_content_charset() is not None:
                        _from = _from.decode(msg.get_content_charset())
                    else:
                        _from = _from.decode(sg.DEFAULT_CHARSET)
                mail_froms.append(_from)
            # Subject
            tuple_subject_charset = email.header.decode_header(msg['subject'])
            subject = tuple_subject_charset[0][0]
            charset = tuple_subject_charset[0][1]
            # Use the embedded charset in the subject if any
            if isinstance(subject, bytes):
                if charset is not None:
                    charset = 'mac-roman' if (charset == 'macintosh') else charset # Dirty hack for really old Apple mail clients (< OS X)
                    subject = subject.decode(charset)
                # Else use any global charset for the mail
                elif msg.get_content_charset() is not None:
                    subject = subject.decode(msg.get_content_charset())
                else:
                    subject = subject.decode(sg.DEFAULT_CHARSET)
            mail_subject = subject
            # Body
            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        payload = part.get_payload(decode=True)
                        if payload is not None and part.get_content_charset() is not None:
                            body += payload.decode(part.get_content_charset())
                        elif payload is not None:
                            body += payload.decode(sg.DEFAULT_CHARSET)
            else:
                body = msg.get_payload(decode=True)
                if msg.get_content_charset() is not None:
                    body = body.decode(msg.get_content_charset())
                else:
                    body = body.decode(sg.DEFAULT_CHARSET)
            mail_body = body
        except Exception as e:
            sg.logger.error('Failed to parse a mail: %s' % e)
        # Just in case some htmlentities were put in the mail...
        mail_body = html.unescape(mail_body) if mail_body is not None else mail_body
        # Result
        return mail_subject, mail_body, mail_froms

    # Utility regexps loader
    def __load_regexps_section(self, sections):
        res = []
        for section in sections:
            res = sum([res, [(k, re.compile(v)) for (k, v) in sg.regex[section].items()]], [])
        return res
    
    def __match_first_regexp(self, regexps, payload):
        for (k, r) in regexps:
            match = r.search(payload)
            if match is not None:
                return k, match.groupdict()
        return None, None
    
    # Main regexp dispatcher and CLASS.populate dispatcher
    def parse(self, subject, body, froms, user):
        if subject is None or body is None:
            return None
        subject = str(subject).replace('\\r', '').replace('\\n', ' ')
        # Dictionary of dictionaries with the results of the regexp matching
        # The first item has all the regexps matching at least one time
        # The following items are for occurences of regexps matching several times
        # At the end all the regexps of the first item not in the others are copied
        res = {0: {}}
        # Loop over the regexp for ignored subject matching
        ignored_regexps = self.__load_regexps_section([sg.CONF_SECTION_IGNORED_SUBJECTS])
        (key, res[0]) = self.__match_first_regexp(ignored_regexps, subject)
        if key is not None: 
            sg.logger.warning('Ignored mail \'%s\', aborting...' % subject)
            return None
        # Loop over the regexp for subject matching
        regexps = self.__load_regexps_section([sg.CONF_SECTION_SUBJECTS])
        (key, res[0]) = self.__match_first_regexp(regexps, subject)
        if key is None:
            sg.logger.warning('No regexp matching mail subject \'%s\', aborting...' % subject)
            return None
        sg.logger.info('Found \'%s\', processing...' % (key))
        # Routine is called based on key, which must be 'CLASS(_\w+)?'
        # formated, for CLASS.build or CLASS.build_\1 to be called.
        # This is probably dangerous behavior but since no people should be
        # allowed to access the .yaml config file without having also access to
        # this piece of code, this seems a nice code/logic factoring feature.
        split = key.split('_', 1)
        _class = split[0]
        _method = 'build' if len(split) == 1 else 'build_' + split[1].lower()
        # The .yaml config file must also have a section named as the
        # key that previously matched or at least the class name with all the
        # associated regexps to match in the mail
        regexps = self.__load_regexps_section([sg.CONF_SECTION_COMMON, _class])
        matchs = [(k, r.finditer(body)) for (k, r) in regexps]
        # We build a base event with the regexps that matched only once (first entry in res dictionnary)
        # And a list of events with the regexps that matched several time in the following entries of res dictionnary
        FLAG_EXCLUDE = 'FLAG_EXCLUDE'
        FLAG_CHECK_EXCLUDES = 'FLAG_CHECK_EXCLUDES'
        excludes = []
        for (key, matchall) in matchs:
            # Filter out any excluded match for this regexp and count the number of resulting items to process (in a new set)
            c = 0
            matchall_filtered = []
            for match in matchall:
                if match is not None:
                    if FLAG_EXCLUDE in match.groupdict(): # If an exclude is flagged, add it for next iterations (following regexp matchs at this position won't be processed)
                        excludes.append((match.start(), match.end()))
                    if len(excludes) == 0 or FLAG_CHECK_EXCLUDES not in match.groupdict() or not any((match.start() >= s and match.end() <= e) for (s, e) in excludes):
                        matchall_filtered.append(match)
                        c += 1
            # Populate the entries
            i = 1 if c > 1 else 0
            for match in matchall_filtered:
                if i not in res:
                    res[i] = {}
                res[i].update(match.groupdict())
                i += 1
        n = len(res)
        # Look for any DUPLICATE flag (parent object will lose its flag but child object will keep it and should be specialy processed in build methods)
        FLAGS_DUPLICATE = ['capa_dead']
        for i in iter(range(n)):
            if any((flag in res[i] and res[i][flag] is not None) for flag in FLAGS_DUPLICATE):
                res[len(res)] = res[i].copy()
                for flag in FLAGS_DUPLICATE:
                    del res[i][flag]
        # Update all the (not duplicated) events with the attrs (not filtered) from the first one
        ATTRS_ONLY_ON_BASE_EVENT = ['px', 'mm', 'rm']
        if n > 1:
            for (key, value) in res[0].items():
                for (i, values) in res.items():
                    if i == 1 or (i > 1 and not key in ATTRS_ONLY_ON_BASE_EVENT):
                        if not key in values:
                            res[i].update({key: value})
            del res[0]
        # Finally, create and populate the object using the dictionary of named group that matched
        objs = []
        for value_set in res.values():
            try:
                obj = globals()[_class]()
            except KeyError as e:
                sg.logger.error('No class %s imported for an allowed parsing, aborting...' % _class)
                return None
            for key in value_set:
                setattr(obj, key, value_set[key])
            obj.mail_subject = subject
            obj.mail_body = body
            # If we did not find the owner of the mail we fix it (followers mail)
            if hasattr(obj, 'owber_id') and obj.owner_id is None:
                obj.owner_id = user.id
            # If the user has a personal mail, check the 'from' header for it
            if not isinstance(obj, MailHelper) and user.user_mail is not None and user.user_mail != '' and not any('bot@mountyhall.com' in f for f in froms):
                if not any(user.user_mail in f for f in froms):
                    sg.logger.warning('No match between \'from\' header and the mail user, rejecting...')
                    continue # COMMENT ME FOR DEBUG ONLY
            # Also do any additional logic related (.build methods)
            if hasattr(globals()[_class], _method) and callable(getattr(globals()[_class], _method)):
                getattr(obj, _method)()
            else:
                obj.build()
            objs.append(obj)
        return objs
