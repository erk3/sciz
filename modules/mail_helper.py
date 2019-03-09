#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import modules.globals as sg


# CLASS DEFINITION
class MailHelper:

    # Constructor
    def __init__(self):
        self.load_conf()
        self.smtp = None
        try:
            self.smtp = smtplib.SMTP(self.smtp_host, self.smtp_port, None, 5)
            self.smtp.ehlo()
            if self.smtp_tls:
                self.smtp.starttls()
                self.smtp.ehlo()
            # self.smtp.login(self.smtp_from, self.smtp_pwd)
        except Exception as e:
            sg.logger.error('Failed to bind to smtp server: %s' % str(e))

    # Configuration loader
    def load_conf(self):
        self.smtp_host = sg.conf[sg.CONF_SMTP_SECTION][sg.CONF_SMTP_HOST]
        self.smtp_port = sg.conf[sg.CONF_SMTP_SECTION][sg.CONF_SMTP_PORT]
        self.smtp_tls = sg.conf[sg.CONF_SMTP_SECTION][sg.CONF_SMTP_TLS]
        self.smtp_from = sg.conf[sg.CONF_SMTP_SECTION][sg.CONF_SMTP_FROM]
        self.smtp_pwd = sg.conf[sg.CONF_SMTP_SECTION][sg.CONF_SMTP_PWD]
   
    def build_gmail(self):
        if not hasattr(self, 'sender') or not hasattr(self, 'code'):
            sg.logger.warning('Detected GMAIL but failed to parse sender or code...')
            return
        sender = self.sender
        code = self.code
        # Build the answer
        subject = '[SCIZ] Code de confirmation de transfert GMAIL'
        text = 'Votre code de transfert GMAIL pour %s est : %s' % (sg.user.mail, code)
        html = '''
        <html>
            <head></head>
            <body>
                <p>Votre code de transfert pour %s est : %s</p>
            </body>
        </html>
        ''' % (sg.user.mail, code)
        # Send the mail
        self.send_mail(sender, subject, text, html)

    def build_yahoo(self):
        if not hasattr(self, 'link'):
            sg.logger.warning('Detected YAHOO but failed to parse link...')
            return
        link = self.link
        # Build the answer
        subject = '[SCIZ] Lien de confirmation de transfert YAHOO'
        text = 'Votre code de transfert YAHOO pour %s est : %s' % (sg.user.mail, link)
        html = '''
        <html>
            <head></head>
            <body>
                <p>Votre lien de transfert pour %s est : %s</p>
            </body>
        </html>
        ''' % (sg.user.mail, link)
        # Send the mail
        self.send_mail(None, subject, text, html)

    def send_mail(self, to, subject, body_text, body_html):
        if self.smtp is None:
            sg.logger.error('An attempt was made to send a mail but no previous bind to a SMTP server was successful')
            return
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.smtp_from
        msg['To'] = to if to is not None else sg.user.user_mail
        msg.attach(MIMEText(body_text, 'plain'))
        msg.attach(MIMEText(body_html, 'html'))
        if msg['To'] is not None:
            self.smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
        else:
            sg.logger.warning('No address to send back...')

    def __del__(self):
        if self.smtp:
            self.smtp.quit()
