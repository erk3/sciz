#   !/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import os, errno
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Table, Column, Integer, ForeignKey

# SqlAlchemyBase
SqlAlchemyBase = declarative_base()

# Utils
def createDirName(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

def boolean2French(boolean):
    if isinstance (boolean, bool):
        return 'Oui' if boolean else 'Non'
    return boolean

def parseFrenchBoolean(boolean):
    if isinstance (boolean, str) or isinstance(boolean, unicode):
        v = boolean.strip().lower()
        if v == 'oui':
            return True
        elif v == 'non':
            return False
    return boolean

def format_time(val, form=None):
    form = form if form else '@%H:%M:%S'
    return val.strftime(form) 

def copy_properties(src, dst, names, with_none):
    for n in names:
        if hasattr(src, n):
            v = getattr(src, n)
            if (v != None or with_none):
                setattr(dst, n, v)

def do_unless_none(fnc, lst):
    lst = filter(lambda x: x!=None, lst)
    lst = [int(x) for x in lst]
    return (fnc)(lst) if len(lst) != 0 else None

def str_min_max(min, max):
    if (min != None and max == None):
        return '>' + str(min)
    elif (min == None and max != None):
        return '<' + str(max)
    elif (min != max):
        return str(min) + '-' + str(max)
    elif (min != None): # min = max
        return str(min)
    else:
        return None

def none_sorter(x, arg):
    if hasattr(x, arg):
        return (getattr(x, arg) is None, getattr(x, arg))
    else:
        None

def pretty_print(obj, short, attrs=None):
    section = obj.__class__.__name__.lower() + '_format'
    if config.has_section(section):
        pp = obj.stringify(config.items(section), short, attrs).encode(DEFAULT_CHARSET)
        return pp
    else:
        logger.error('No section \'%s\' in config for printing \'%s\' class' % (section, obj.__class__.__name__))
        return None


# GENERAL CONF
DEFAULT_CONF_FILE               = "sciz.ini"
DEFAULT_CHARSET                 = "utf-8"

# LOG SECTION
CONF_LOG_SECTION                = "log"
CONF_LOG_FILE           	= "file"
CONF_LOG_FILE_MAX_SIZE  	= "file_max_size"
CONF_LOG_FORMATTER      	= "formatter"
CONF_LOG_DEFAULT_LEVEL  	= "default_level"

# SMTP SECTION
CONF_SMTP_SECTION       	= "smtp"
CONF_SMTP_FROM          	= "from"
CONF_SMTP_HOST          	= "host"
CONF_SMTP_PORT          	= "port"
CONF_SMTP_PWD            	= "pwd"

# MAIL SECTION
CONF_MAIL_SECTION       	= "mail"
CONF_MAIL_DOMAIN_NAME          	= "domain_name"
CONF_MAIL_PATH          	= "maildirs_base_path"
CONF_MAIL_POSTFIX_CONF_FILE    	= "postfix_accounts_conf_file"

# JSON SECTION
CONF_JSON_SECTION       	= "json"
CONF_JSON_USERS_TAG     	= "users_tag"
CONF_JSON_USERS_ID      	= "users_id"

# MH SECTION
CONF_MH_SECTION         	= "mh"
CONF_SP_URL             	= "sp_url"
CONF_SP_ID              	= "sp_p_id"
CONF_SP_APIKEY          	= "sp_p_apikey"
CONF_SP_PROFIL2         	= "profil2_path"
CONF_SP_CARACT          	= "caract_path"
CONF_FTP_URL            	= "ftp_url"
CONF_FTP_TROLLS2        	= "trolls2_path"
CONF_FTP_MONSTRES       	= "monstres_path"

# DB SECTION
CONF_DB_SECTION         	= "db"
CONF_DB_HOST            	= "host"
CONF_DB_PORT            	= "port"
CONF_DB_NAME                    = "name"
CONF_DB_USER            	= "user"
CONF_DB_PASS            	= "passwd"

# INSTANCE SECTION
CONF_INSTANCE_SECTION           = "instance"
CONF_INSTANCE_FTP_REFRESH       = "ftp_refresh"
CONF_INSTANCE_MAIL_REFRESH 	= "mail_refresh"
CONF_INSTANCE_HOOK_REFRESH 	= "hook_refresh"
CONF_INSTANCE_MAIL_RETENTION 	= "mail_max_retention"

# SECTION
CONF_SECTION_COMMON             = "common"
CONF_SECTION_SUBJECTS           = "subjects"
CONF_SECTION_IGNORED_SUBJECTS   = "ignored_subjects"
CONF_SECTION_BATTLE             = "battle"
CONF_NOTIF_TIME                 = "re_time"
CONF_NOTIF_VIE                  = "re_vie"

# GROUP SECTION
CONF_GROUP_BATTLE_FORMAT      	= "battle_format"
CONF_GROUP_TROLL_FORMAT      	= "troll_format"
CONF_GROUP_MOB_FORMAT      	= "mob_format"
CONF_GROUP_CDM_FORMAT      	= "cdm_format"
CONF_GROUP_PIEGE_FORMAT      	= "piege_format"
