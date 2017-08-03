#   !/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
from sqlalchemy.ext.declarative import declarative_base 

# SqlAlchemyBase
SqlAlchemyBase = declarative_base()

# Utils
def parseFrenchBoolean(boolean):
    if isinstance (boolean, str):
        if boolean.lower() == 'oui':
            return True
        elif boolean.lower() == 'non':
            return False
    return None

def format_time(val):
    return str(val.hour).zfill(2) + ':' + str(val.minute).zfill(2) + ':' + str(val.second).zfill(2)

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
    elif (min != None):
        return str(min)
    else:
        return None

# GENERAL CONF
DEFAULT_CONF_FILE       = "sciz.ini"
DEFAULT_CHARSET         = "utf-8"

# APP SECTION
CONF_APP_SECTION        = "app"
CONF_APP_NAME           = "name"

# MAIL SECTION
CONF_MAIL_SECTION       = "mail"
CONF_MAIL_PATH          = "maildir_path"
CONF_MAIL_CDM_RE        = "reg_cdm_subject"
CONF_MAIL_ATT_RE        = "reg_att_subject"
CONF_MAIL_DEF_RE        = "reg_def_subject"
CONF_EVENT_TROLL_RE     = "reg_event_troll"
CONF_EVENT_TIME_RE      = "reg_event_time"
CONF_EVENT_TYPE_RE      = "reg_event_type"

# JSON SECTION
CONF_JSON_SECTION       = "json"
CONF_JSON_USERS_TAG     = "users_tag"
CONF_JSON_USERS_ID      = "users_id"

# MH SECTION
CONF_MH_SECTION         = "mh"
CONF_SP_URL             = "sp_url"
CONF_SP_ID              = "sp_p_id"
CONF_SP_APIKEY          = "sp_p_apikey"
CONF_SP_PROFIL2         = "profil2_path"
CONF_SP_CARACT          = "caract_path"
CONF_FTP_URL            = "ftp_url"
CONF_FTP_TROLLS2        = "trolls2_path"
CONF_FTP_MONSTRES       = "monstres_path"

# BATTLE EVENT SECTION
CONF_ATT_SECTION        = "att"
CONF_DEF_SECTION        = "def"
CONF_EVENT_DESC_RE      = "reg_event_desc"
CONF_EVENT_ATT_RE       = "reg_event_att"
CONF_EVENT_ESQ_RE       = "reg_event_esq"
CONF_EVENT_DEG_RE       = "reg_event_deg"
CONF_EVENT_PV_RE        = "reg_event_pv"
CONF_EVENT_SR_RE        = "reg_event_sr"
CONF_EVENT_RESI_RE      = "reg_event_resi"
CONF_EVENT_VIE_RE       = "reg_event_vie"
CONF_EVENT_CAPA_RE      = "reg_event_capa"
CONF_EVENT_CAPA_EFFET_RE= "reg_event_capa_effet"
CONF_EVENT_CAPA_TOUR_RE = "reg_event_capa_tour"

# CDM SECTION
CONF_CDM_SECTION        = "cdm"
CONF_CDM_DESC_RE        = "reg_cdm_desc"  
CONF_CDM_TYPE_RE        = "reg_cdm_type"  
CONF_CDM_NIV_RE         = "reg_cdm_niv"  
CONF_CDM_PV_RE          = "reg_cdm_pv"  
CONF_CDM_BLESSURE_RE    = "reg_cdm_blessure"  
CONF_CDM_ATT_RE         = "reg_cdm_att"  
CONF_CDM_ESQ_RE         = "reg_cdm_esq"  
CONF_CDM_DEG_RE         = "reg_cdm_deg"  
CONF_CDM_REG_RE         = "reg_cdm_reg"  
CONF_CDM_ARM_RE         = "reg_cdm_arm"  
CONF_CDM_VUE_RE         = "reg_cdm_vue"  
CONF_CDM_MM_RE          = "reg_cdm_mm"  
CONF_CDM_RM_RE          = "reg_cdm_rm"  
CONF_CDM_CAPA_RE        = "reg_cdm_capa"  
CONF_CDM_NB_ATT_RE      = "reg_cdm_nb_att"  
CONF_CDM_VIT_DEP_RE     = "reg_cdm_vit_dep"  
CONF_CDM_VLC_RE         = "reg_cdm_vlc"  
CONF_CDM_ATT_DIST_RE    = "reg_cdm_att_dist"  

# DB SECTION
CONF_DB_SECTION         = "db"
CONF_DB_HOST            = "host"
CONF_DB_PORT            = "port"
CONF_DB_NAME            = "name"
CONF_DB_USER            = "user"
CONF_DB_PASS            = "passwd"

# PRINT SECTION
CONF_PRINT_SECTION      = "print"
CONF_PRINT_SEP          = "stats_sep"
CONF_PRINT_NIV          = "stat_niv"
CONF_PRINT_PV           = "stat_pv"
CONF_PRINT_ATT          = "stat_att"
CONF_PRINT_ESQ          = "stat_esq"
CONF_PRINT_DEG          = "stat_deg"
CONF_PRINT_REG          = "stat_reg"
CONF_PRINT_VUE          = "stat_vue"
CONF_PRINT_MM           = "stat_mm"
CONF_PRINT_RM           = "stat_rm"
CONF_PRINT_ARM_PHY      = "stat_arm_phy"
CONF_PRINT_CAPA         = "stat_capa"
CONF_PRINT_VLC          = "stat_vlc"
CONF_PRINT_ATT_DIST     = "stat_att_dist"
CONF_PRINT_VIT          = "stat_vit"
CONF_PRINT_NB_ATT       = "stat_nb_att"
CONF_MOB_FULL           = "mob_head_full"
CONF_MOB_SHORT          = "mob_short"
CONF_CDM_FULL           = "cdm_head_full"
CONF_CDM_SHORT          = "cdm_short"
CONF_BATTLE_EVENT_SHORT = "battle_event_short"
CONF_BATTLE_EVENT_FULL  = "battle_event_full"






