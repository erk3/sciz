#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from modules.mail_walker import MailWalker
from modules.mh_caller import MhCaller
from classes.user import User
from classes.user_mh_call import MhCall
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import datetime, os, time, re
import modules.globals as sg


# CLASS DEFINITION 
class AdminHelper:

    # Constructor
    def __init__(self):
        self.load_conf()
        sg.wk = MailWalker()
        sg.mc = MhCaller()

    # Configuration loader
    def load_conf(self):
        self.mailDirPath = sg.conf[sg.CONF_MAIL_SECTION][sg.CONF_MAIL_PATH]
        self.ftpRefresh = sg.conf[sg.CONF_INSTANCE_SECTION][sg.CONF_INSTANCE_FTP_REFRESH]
        self.mailRetention = sg.conf[sg.CONF_INSTANCE_SECTION][sg.CONF_INSTANCE_MAIL_RETENTION]

    # Initializer, create the SQL schema
    def init(self):
        sg.db.init()

    # Mail walker
    def walk(self):
        # One time call
        if sg.user is not None:
            sg.logger.info('Walking the mails of user %s...' % sg.user.id)
            sg.wk.walk()
            return
        # Watchdog setup
        global locked
        # Watchdog definition
        class MailFileHandler(FileSystemEventHandler):

            def __init__(self, mailDirPath):
                super()
                self.mailDirPath = mailDirPath

            def on_created(self, event):
                if not event.is_directory and os.sep + 'new' + os.sep in event.src_path:
                    self.process(event.src_path)

            def on_moved(self, event):
                if not event.is_directory and os.sep + 'new' + os.sep in event.dest_path:
                    self.process(event.dest_path)

            def on_modified(self, event):
                self.on_created(event)

            def on_deleted(self, event):
                pass

            def process(self, path):
                global locked
                while locked:
                    time.sleep(3)
                locked = True
                if os.path.exists(path): # Mail could have been processed while waiting
                    try:
                        m = re.search('%s(%s)?(?P<user_id>[^\.%s]+)' % (self.mailDirPath, os.sep, os.sep), path)
                        user_id = m.group('user_id')
                        sg.logger.info('New mails for user %s !' % user_id)
                        sg.user = sg.db.session.query(User).get(user_id)
                        sg.wk.walk()
                    except Exception as e:
                        sg.db.session.rollback()
                        sg.logger.exception(e)
                locked = False
        # Watchdog start
        locked = False
        mfh, obs = MailFileHandler(self.mailDirPath), Observer()
        obs.schedule(mfh, self.mailDirPath, recursive=True)
        obs.start()
        try:
            while True:
                time.sleep(3)
        except KeyboardInterrupt:
            obs.stop()
        obs.join()

    # MH Updater
    def update(self, scripts=None):
        # One time call for a SP
        if sg.user is not None:
            sg.logger.info('Calling MH for user %s...' % sg.user.id)
            sg.mc.call(sg.user, scripts)
            return
        # Infinite refresh of FTP and SP
        last_ftp_call = None
        while True:
            now = datetime.datetime.now()
            if sg.time_in_between(now.time(), datetime.time(4), datetime.time(5)):
                # MH is down between 4am and 5am
                time.sleep(60)
                continue
            if last_ftp_call is None or (now - last_ftp_call).total_seconds() >= self.ftpRefresh * 60:
                try:
                    sg.mc.trolls2_ftp_call()
                    sg.mc.monstres_ftp_call()
                    sg.mc.tresors_ftp_call()
                    sg.mc.capas_ftp_call()
                    sg.mc.events_ftp_call()
                    last_ftp_call = now
                except Exception as e:
                    sg.logger.warning('Error while calling MH FTP : %s' % e)
                    sg.logger.exception(e)
                    sg.db.session.rollback()
            users = sg.db.session.query(User).filter(User.mh_api_key is not None, User.mh_api_key != '').all()
            for user in users:
                try:
                    if user.should_refresh_dynamic_sp:
                        last_call = user.mh_calls.filter(MhCall.status == 0, MhCall.type == 'Dynamique').order_by(MhCall.time.desc()).first()
                        if last_call is None or last_call.nom == 'Vue2':
                            called = sg.mc.profil4_sp_call(user)
                        else:
                            called = sg.mc.vue2_sp_call(user)
                        # This routine is heavy load, we keep it cool for a little while
                        if called:
                            time.sleep(1)
                except Exception as e:
                    sg.logger.warning('Error while calling MH SP for user %s : %s' % (user.id, e))
                    sg.logger.exception(e)
                    sg.db.session.rollback()
            time.sleep(60)

    # Vacuum cleaner
    def vacuum(self):
        # Mail directory purge
        last_mail_purge = None
        while True:
            now = datetime.datetime.now()
            if last_mail_purge is None or (now - last_mail_purge).total_seconds() >= self.mailRetention * 60:
                users = sg.db.session.query(User).all()
                for user in users:
                    sg.wk.purge(user, 'archive')
            time.sleep(60)
