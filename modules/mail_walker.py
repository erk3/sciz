#! /usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from modules.mail_parser import MailParser
from modules.mail_helper import MailHelper
from operator import itemgetter
import email, mailbox, os, datetime, re
import modules.globals as sg


# CLASS DEFINITION
class MailWalker:

    # Constructor
    def __init__(self):
        self.mp = MailParser()
        self.load_conf()
        
    # Configuration loader
    def load_conf(self):
        self.mailDirPath = sg.conf[sg.CONF_MAIL_SECTION][sg.CONF_MAIL_PATH]
        self.mailMaxRetention = sg.conf[sg.CONF_INSTANCE_SECTION][sg.CONF_INSTANCE_MAIL_RETENTION]

    # Archive routine
    def archive(self, user, file_name, subdir):
        user = user if user is not None else sg.user
        new_file = self.mailDirPath + os.sep + user.mail + os.sep + subdir + os.sep + os.path.basename(file_name)
        try:
            sg.createDirName(new_file)
            os.rename(file_name, new_file)
        except (OSError, IOError) as e:
            sg.logger.error('Fail to move mail \'%s\' to \'%s\'! Error: %s' % (file_name, new_file, e))

    # Purge routine
    def purge(self, user, subdir):
        user = user if user is not None else sg.user
        dir_path = self.mailDirPath + os.sep + user.mail + os.sep + subdir + os.sep
        ago = datetime.datetime.now() - datetime.timedelta(minutes=self.mailMaxRetention)
        try:
            for f in os.listdir(dir_path):
                last_modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(dir_path + os.sep + f))
                if last_modified_date < ago:
                    os.remove(dir_path + os.sep + f)
        except (OSError, IOError) as e:
            sg.logger.warning('Fail to purge \'%s\' mail directory! Error: %s' % (dir_path, e))

    # Walker routine
    def walk(self):
        try:
            sg.db.session = sg.db.new_session()
            # Open the mailbox
            mbox = mailbox.Maildir(self.mailDirPath + os.sep + sg.user.mail)
            # Build a sorted list of key-message by 'Date' header #RFC822
            sorted_mbox = sorted(mbox.iteritems(), key=lambda x: email.utils.parsedate(x[1].get('Date')))
            # Then get the actuals mails
            actual_mails = [(mbox.get_file(item[0])._file.name, email.message_from_string(mbox.get_string(item[0]))) for item in sorted_mbox]
            parsed_mails = [(file_path, self.mp.parse_mail(mail)) for (file_path, mail) in actual_mails]
            # Then re-sort by MH date, then by remaining life points (multiple events at same time)
            re_time = re.compile(sg.regex[sg.CONF_SECTION_COMMON][sg.CONF_NOTIF_TIME])
            re_vie = re.compile(sg.regex[sg.CONF_SECTION_BATTLE][sg.CONF_NOTIF_VIE])
            parsed_mails_with_attrs = [(n, s, b, f, re_time.search(b) if b else None, re_vie.search(b) if b else None) for (n, (s, b, f)) in parsed_mails]
            parsed_mails_with_attrs = [(n, s, b, f, datetime.datetime.strptime(t.groupdict()['time'], '%d/%m/%Y %H:%M:%S') if t else datetime.datetime.now(), int(v.groupdict()['vie']) if v else 0) for (n, s, b, f, t, v) in parsed_mails_with_attrs]
            sorted_mails = sorted(parsed_mails_with_attrs, key=itemgetter(4, 5))
            # Finally walk over the mails
            for file_path, subject, body, froms, time, vie in sorted_mails:
                try:
                    objs = self.mp.parse(subject, body, froms, sg.user)
                    if objs == 'UNHANDLED':
                        self.archive(sg.user, file_path, 'unhandled')
                    elif objs is not None:
                        if not type(objs) is list: objs = [objs]
                        for obj in objs:
                            if not isinstance(obj, MailHelper):
                                obj = sg.db.upsert(obj)
                                # DEBUG ONLY
                                #session, obj = sg.db.rebind(obj)
                                #print(sg.no.stringify(obj), os.linesep)
                                #session.close()
                        # Archive the mail
                        self.archive(sg.user, file_path, 'archive')
                    else:
                        # Unrecognized or ignored mail, delete it immediatly
                        os.remove(file_path)
                # If anything goes wrong parsing a mail, it will land here (hopefully)
                except Exception as e:
                    sg.logger.error('Failed to handle mail \'%s\'' % file_path, exc_info=True)
                    self.archive(sg.user, file_path, 'error')
                    sg.logger.exception(e)
                    sg.db.session.rollback()
            # Push reverse hook
            if sg.db.session is not None:
                sg.db.session.close()
            sg.db.session, sg.user = sg.db.rebind(sg.user)
            for p in sg.user.partages_actifs + [sg.user.partage_perso]:
                if p.coterie is not None and p.coterie.hook_miaou is not None:
                    p.coterie.hook_miaou.trigger(False)
        except (OSError, IOError, mailbox.Error) as e:
            sg.logger.error('Fail to scan mail directory! Error: %s' % e)
        finally:
            if sg.db.session is not None:
                sg.db.session.close()
