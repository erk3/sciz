#!/usr/bin/env python3
#coding: utf-8

# IMPORTS
from sqlalchemy.ext.declarative import declarative_base
import os, errno, itertools, re, unidecode

# GLOBALS
sqlalchemybase = declarative_base()
sciz = None # Kind of a singleton
conf = None # Main configuration
regex = None # Main regexps
format = None # Main formats
formulas = None # Main formats
logger = None # Main logger
db = None # Main database
user = None # Main/Current user
ah = None # AdminHelper
wk = None # MailWalker
ws = None # WebServer
mc = None # MhCaller
req = None # Requester
no = None # Notifier

# GENERAL CONF
DEFAULT_CHARSET                 = 'utf-8'

# LOG SECTION
CONF_LOG_SECTION                = 'log'
CONF_LOG_FILE                   = 'file'
CONF_LOG_FILE_MAX_SIZE          = 'file_max_size'
CONF_LOG_FORMATTER              = 'formatter'
CONF_LOG_DEFAULT_LEVEL          = 'default_level'

# SMTP SECTION
CONF_SMTP_SECTION               = 'smtp'
CONF_SMTP_FROM                  = 'from'
CONF_SMTP_HOST                  = 'host'
CONF_SMTP_PORT                  = 'port'
CONF_SMTP_TLS                   = 'tls'
CONF_SMTP_PWD                   = 'pwd'

# MAIL SECTION
CONF_MAIL_SECTION               = 'mail'
CONF_MAIL_DOMAIN_NAME           = 'domain_name'
CONF_MAIL_PATH                  = 'maildirs_base_path'
CONF_MAIL_POSTFIX_CONF_FILE     = 'postfix_accounts_conf_file'

# MH SECTION
CONF_MH_SECTION                 = 'mh'
CONF_OAUTH_SERVER_METADATA_URL  = 'oauth_server_metadata_url'
CONF_OAUTH_CLIENT_ID            = 'oauth_client_id'
CONF_OAUTH_CLIENT_SECRET        = 'oauth_client_secret'
CONF_OAUTH_CLIENT_SCOPE         = 'oauth_client_scope'
CONF_SP_URL                     = 'sp_url'
CONF_SP_ID                      = 'sp_p_id'
CONF_SP_APIKEY                  = 'sp_p_apikey'
CONF_SP_PROFIL4                 = 'profil4_path'
CONF_SP_VUE2                    = 'vue2_path'
CONF_SP_VUE2_TRESORS            = 'sp_p_tresors'
CONF_SP_VUE2_CHAMPIS            = 'sp_p_champis'
CONF_SP_VUE2_LIEUX              = 'sp_p_lieux'
CONF_FTP_URL                    = 'ftp_url'
CONF_FTP_TROLLS2                = 'trolls2_path'
CONF_FTP_MONSTRES               = 'monstres_path'
CONF_FTP_TRESORS                = 'tresors_path'
CONF_FTP_SORTS                  = 'sorts_path'
CONF_FTP_COMPS                  = 'comps_path'
CONF_FTP_GUILDES                = 'guildes_path'
CONF_FTP_EVENTS                 = 'events_path'
CONF_LINK_TROLL                 = 'troll_link'
CONF_LINK_MOB                   = 'mob_link'
CONF_LINK_TRESOR                = 'tresor_link'
CONF_LINK_MP                    = 'mp_link'
CONF_LINK_PX                    = 'px_link'

# WEB SECTION
CONF_WEB_SECTION                = 'web'
CONF_WEB_PORT                   = 'port'
CONF_WEB_SECRET                 = 'secret'
CONF_WEB_DOMAIN                 = 'domain'
CONF_WEB_TLS                    = 'tls'

# DB SECTION
CONF_DB_SECTION                 = 'db'
CONF_DB_HOST                    = 'host'
CONF_DB_PORT                    = 'port'
CONF_DB_NAME                    = 'name'
CONF_DB_USER                    = 'user'
CONF_DB_PASS                    = 'passwd'

# INSTANCE SECTION
CONF_INSTANCE_SECTION           = 'instance'
CONF_INSTANCE_FTP_REFRESH       = 'ftp_refresh_rate'
CONF_INSTANCE_MAIL_RETENTION    = 'mail_max_retention'
CONF_INSTANCE_REGEX_FILE        = 'regex_filename'
CONF_INSTANCE_FORMAT_FILE       = 'default_format_filename'
CONF_INSTANCE_FORMULA_FILE      = 'formula_filename'

# HOOK SECTION
CONF_HOOK_SECTION               = 'hooks'
CONF_HOOK_URL                   = 'URL'

# SCIZ HELP
CONF_SCIZ_HELP                  = 'sciz_help'

# REGEX SECTION
CONF_SECTION_COMMON             = 'common'
CONF_SECTION_SUBJECTS           = 'subjects'
CONF_SECTION_IGNORED_SUBJECTS   = 'ignored_subjects'
CONF_SECTION_MAIL               = 'MailHelper'
CONF_SECTION_BATTLE             = 'battleEvent'
CONF_NOTIF_TIME                 = 're_time'
CONF_NOTIF_VIE                  = 're_vie'

# FORMAT SECTION
CONF_FORMAT_NOTIFICATION        = 'Notification'
CONF_FORMAT_BUILDED_ATTRS       = 'Attributs construits'
CONF_FORMAT_ATTRS               = 'Attributs'
CONF_FORMAT_ATTRS_ATTR          = 'Attribut'
CONF_FORMAT_ATTRS_VALUE         = 'Valeur'
CONF_FORMAT_ATTRS_PREFIX        = 'Préfixe'
CONF_FORMAT_ATTRS_SUFFIX        = 'Suffixe'
CONF_FORMAT_ATTRS_TIME          = 'Format temporel'
CONF_FORMAT_ABREVIATIONS        = 'Abréviations'
CONF_FORMAT_FILTRE              = 'Filtres'

# FORMULA SECTION
CONF_FORMULA_TEXT               = 'Texte'
CONF_FORMULA_BASE               = 'Base'
CONF_FORMULA_BONUS              = 'Bonus'


# UTILS
def createDirName(file_path):
    if not os.path.exists(os.path.dirname(file_path)) and os.sep in file_path:
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


def boolean2French(boolean, val=None):
    if isinstance (boolean, bool):
        if val is None:
            return 'Oui' if boolean else 'Non'
        else:
            return val if boolean else ''
    return boolean


def parseFrenchBoolean(boolean):
    if isinstance (boolean, str):
        v = boolean.strip().lower()
        if v == 'oui':
            return True
        elif v == 'non':
            return False
    return boolean


def format_time(val, form=None):
    form = form if form else '%d/%m/%Y %H:%M:%S'
    if val:
        return val.strftime(form)
    return None


def minutes_to_time(minutes):
    if minutes:
        return '{:02d}h{:02d}m'.format(*divmod(minutes, 60))
    return None


def time_in_between(now, start, end):
    if start <= end:
        return start <= now < end
    else:
        return start <= now or now < end


def copy_properties(src, dst, names, with_none):
    for n in names:
        if hasattr(src, n):
            v = getattr(src, n)
            if v is not None or with_none:
                setattr(dst, n, v)


def do_unless_none(fnc, lst):
    lst = filter(lambda x: x is not None, lst)
    lst = [int(x) for x in lst]
    return fnc(lst) if len(lst) != 0 else None


def str_min_max(min, max):
    if min is not None and max is None:
        return '>' + str(min)
    elif min is None and max is not None:
        return '<' + str(max)
    elif min != max:
        return str(min) + '-' + str(max)
    elif min is not None: # min = max
        return str(min)
    else:
        return ''


def str_phy_mag(phy, mag):
    if phy is not None and mag is None:
        return f"{phy:+d}"
    elif phy is None and mag is not None:
        return f"{mag:+d}"
    elif phy is not None: # phy and mag
        return f"{phy:+d}/{mag:+d}"
    else:
        return ''


def none_sorter(x, arg):
    if hasattr(x, arg):
        return (getattr(x, arg) is None, getattr(x, arg))
    return None


def re_partition_multiple(content, separator):
    res = []
    separator_match = re.search(separator, content)
    if separator_match is None:
        return [content]
    while separator_match is not None:
        matched_separator = separator_match.group(0)
        parts = content.split(matched_separator, 1)
        if parts[0] != '' and parts[0] != ' ':
            res.append(parts[0])
        if matched_separator != ' ':
            res.append(matched_separator)
        content = parts[1]
        separator_match = re.search(separator, content)
    if parts[1] != '' and parts[1] != ' ':
        res.append(content)
    return res


def zero_out(o, ATTRS_TO_DELETE):
    for attr in ATTRS_TO_DELETE:
        if hasattr(o, attr):
            delattr(o, attr)


def zero_out_but(o, ATTR_TO_KEEP):
    ATTRS_TO_DELETE = []
    for attr in vars(o):
        if not attr.startswith('_') and attr not in ATTR_TO_KEEP:
            ATTRS_TO_DELETE.append(attr)
    for attr in ATTRS_TO_DELETE:
        delattr(o, attr)


def flatten(s):
    return ''.join(list(filter(str.isalnum, unidecode.unidecode(s.lower()))))


row2dictfull = lambda r: {c.name: getattr(r, c.name) for c in list(itertools.chain.from_iterable([m.__table__.columns for m in [type(r)] + list(r.__class__.__bases__)]))}


row2dict = lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns}


row2dictWithoutNone = lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns if getattr(r, c.name) is not None}

def max_datetime(a, b):
    if a is None: return b
    if b is None: return a
    return max(a, b)
