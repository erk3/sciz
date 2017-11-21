#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Imports
import smtplib, re, ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import modules.globals as sg

## MailHelper class for SCIZ
class MailHelper:

    # Constructor
    def __init__(self):
        self.check_conf()
        self.smtp = None
        try:
            self.smtp = smtplib.SMTP(self.smtp_host, int(self.smtp_port), None, 5)
            self.smtp.set_debuglevel(1)
            self.smtp.login(self.smtp_from, self.smtp_pwd)
        except Exception as e:
            sg.logger.warning('Failed to bind to smtp server')

    # Configuration loader and checker
    def check_conf(self):
        try:
            self.smtp_host = sg.config.get(sg.CONF_SMTP_SECTION, sg.CONF_SMTP_HOST)
            self.smtp_port = sg.config.get(sg.CONF_SMTP_SECTION, sg.CONF_SMTP_PORT)
            self.smtp_from = sg.config.get(sg.CONF_SMTP_SECTION, sg.CONF_SMTP_FROM)
            self.smtp_pwd = sg.config.get(sg.CONF_SMTP_SECTION, sg.CONF_SMTP_PWD)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error('Fail to load config file! (ConfigParser error: %s)' % (str(e), ))
            raise
    
    def answer_gmail_forward_confirmation(self, subject, body, group=None):
        try:
            re_gmail_desc = sg.config.get(sg.CONF_GMAIL_SECTION, sg.CONF_GMAIL_DESC_RE)
            re_gmail_code = sg.config.get(sg.CONF_GMAIL_SECTION, sg.CONF_GMAIL_CODE_RE)
            re_gmail_desc_en = sg.config.get(sg.CONF_GMAIL_SECTION, sg.CONF_GMAIL_DESC_EN_RE)
            re_gmail_code_en = sg.config.get(sg.CONF_GMAIL_SECTION, sg.CONF_GMAIL_CODE_EN_RE)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error('Fail to load config file! (ConfigParser error: %s)' % (str(e), ))
            raise
        group = group if group else sg.group
        # Get the code and the sender
        res = re.search(re_gmail_desc, body)
        to = res.group(1) if res else None
        if not to:
            res = re.search(re_gmail_desc_en, body)
            to = res.group(1)
        res = re.search(re_gmail_code, body)
        code = res.group(1) if res else None
        if not code:
            res = re.search(re_gmail_code_en, body)
            code = res.group(1)
        # Build the answer
        subject = "[SCIZ] Code de confirmation de transfert GMAIL vers %s" % (group.mail, )
        text = "Votre code de transfert GMAIL pour %s est : %s" % (group.mail, code, )
        html = """\
        <html>
            <head></head>
            <body>
                <p>Votre code de transfert pour %s est : %s</p>
            </body>
        </html>
        """ % (group.mail, code, )
        # Send the mail
        self.send_mail(to, subject, text, html)

    def send_mail(self, to, subject, body_text, body_html):
        if not self.smtp:
            sg.logger.warning('An attempt was made to send a mail but no previous bind to a SMTP server was successful')
            return
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.smtp_from
        msg['To'] = to
        msg.attach(MIMEText(body_text, 'plain'))
        msg.attach(MIMEText(body_html, 'html'))
        self.smtp.sendmail(self.smtp_from, [to], msg.as_string())

    def __del__(self):
        if self.smtp:
            self.smtp.quit()
