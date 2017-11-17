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
    elif (min != None): # min = max
        return str(min)
    else:
        return None

def none_sorter(x, arg):
    if hasattr(x, arg):
        return (getattr(x, arg) is None, getattr(x, arg))
    else:
        None

# GENERAL CONF
DEFAULT_CONF_FILE               = "sciz.ini"
DEFAULT_CHARSET                 = "utf-8"

# LOG SECTION
CONF_LOG_SECTION                = "log"
CONF_LOG_FILE           	= "file"
CONF_LOG_FILE_MAX_SIZE  	= "file_max_size"
CONF_LOG_FORMATTER      	= "formatter"
CONF_LOG_DEFAULT_LEVEL  	= "default_level"

# MAIL SECTION
CONF_MAIL_SECTION       	= "mail"
CONF_MAIL_DOMAIN_NAME          	= "domain_name"
CONF_MAIL_PATH          	= "maildirs_base_path"
CONF_MAIL_POSTFIX_CONF_FILE    	= "postfix_accounts_conf_file"
CONF_MAIL_CDM_RE        	= "reg_cdm_subject"
CONF_MAIL_MSG_RE        	= "reg_msg_subject"
CONF_MAIL_ATT_RE        	= "reg_att_subject"
CONF_MAIL_DEF_RE        	= "reg_def_subject"
CONF_MAIL_ATT_VT_RE      	= "reg_att_vt_subject"
CONF_MAIL_DEF_VT_RE      	= "reg_def_vt_subject"
CONF_MAIL_ATT_HYPNO_RE      	= "reg_att_hypno_subject"
CONF_MAIL_DEF_HYPNO_RE      	= "reg_def_hypno_subject"
CONF_MAIL_ATT_SACRO_RE      	= "reg_att_sacro_subject"
CONF_MAIL_DEF_SACRO_RE      	= "reg_def_sacro_subject"
CONF_MAIL_ATT_EXPLO_RE      	= "reg_att_explo_subject"
CONF_MAIL_DEF_EXPLO_RE      	= "reg_def_explo_subject"
CONF_MAIL_CAPA_RE      	        = "reg_capa_subject"
CONF_MAIL_PIEGE_RE      	= "reg_piege_subject"
CONF_EVENT_TROLL_RE     	= "reg_event_troll"
CONF_EVENT_TIME_RE      	= "reg_event_time"
CONF_EVENT_TYPE_RE      	= "reg_event_type"
CONF_END_MAIL_RE      	        = "reg_end_mail"
CONF_FIRST_HTML_RE      	= "reg_first_html"

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

# BATTLE EVENT SECTION
CONF_ATT_SECTION        	= "att"
CONF_DEF_SECTION        	= "def"
CONF_HYPNO_SECTION      	= "hypno"
CONF_SACRO_SECTION      	= "sacro"
CONF_CAPA_SECTION      	        = "capa"
CONF_VT_SECTION      	        = "vt"
CONF_EXPLO_SECTION      	= "explo"
CONF_EVENT_DESC_RE      	= "reg_event_desc"
CONF_EVENT_ATT_RE       	= "reg_event_att"
CONF_EVENT_ESQ_RE       	= "reg_event_esq"
CONF_EVENT_DEG_RE       	= "reg_event_deg"
CONF_EVENT_PV_RE        	= "reg_event_pv"
CONF_EVENT_SR_RE        	= "reg_event_sr"
CONF_EVENT_RESI_ATT_RE      	= "reg_event_resi_att"
CONF_EVENT_RESI_DEF_RE      	= "reg_event_resi_def"
CONF_EVENT_MORT_ATT_RE      	= "reg_event_mort_att"
CONF_EVENT_MORT_DEF_RE      	= "reg_event_mort_def"
CONF_EVENT_SOIN_ATT_RE      	= "reg_event_soin_att"
CONF_EVENT_SOIN_DEF_RE      	= "reg_event_soin_def"
CONF_EVENT_VIE_RE       	= "reg_event_vie"
CONF_EVENT_BLESSURE_RE       	= "reg_event_blessure"
CONF_EVENT_CAPA_RE      	= "reg_event_capa"
CONF_EVENT_CAPA_EFFET_ATT_RE	= "reg_event_capa_effet_att"
CONF_EVENT_CAPA_EFFET_DEF_RE	= "reg_event_capa_effet_def"
CONF_EVENT_CAPA_TOUR_RE 	= "reg_event_capa_tour"

# PIEGE SECTION
CONF_PIEGE_SECTION        	= "piege"
CONF_PIEGE_DESC_RE        	= "reg_piege_desc"  

# CDM SECTION
CONF_CDM_SECTION        	= "cdm"
CONF_CDM_DESC_RE        	= "reg_cdm_desc"  
CONF_CDM_TYPE_RE        	= "reg_cdm_type"  
CONF_CDM_NIV_RE         	= "reg_cdm_niv"  
CONF_CDM_PV_RE          	= "reg_cdm_pv"  
CONF_CDM_BLESSURE_RE    	= "reg_cdm_blessure"  
CONF_CDM_ATT_RE         	= "reg_cdm_att"  
CONF_CDM_ESQ_RE         	= "reg_cdm_esq"  
CONF_CDM_DEG_RE         	= "reg_cdm_deg"  
CONF_CDM_REG_RE         	= "reg_cdm_reg"  
CONF_CDM_ARM_RE         	= "reg_cdm_arm"  
CONF_CDM_VUE_RE         	= "reg_cdm_vue"  
CONF_CDM_MM_RE          	= "reg_cdm_mm"  
CONF_CDM_RM_RE          	= "reg_cdm_rm"  
CONF_CDM_CAPA_RE        	= "reg_cdm_capa"  
CONF_CDM_NB_ATT_RE      	= "reg_cdm_nb_att"  
CONF_CDM_VIT_DEP_RE     	= "reg_cdm_vit_dep"  
CONF_CDM_VLC_RE         	= "reg_cdm_vlc"  
CONF_CDM_ATT_DIST_RE    	= "reg_cdm_att_dist"  
CONF_CDM_DLA_RE         	= "reg_cdm_dla"
CONF_CDM_TOUR_RE        	= "reg_cdm_tour"
CONF_CDM_CHARGEMENT_RE  	= "reg_cdm_chargement"
CONF_CDM_BONUS_MALUS_RE 	= "reg_cdm_bonus_malus"
CONF_CDM_PORTEE_CAPA_RE 	= "reg_cdm_portee_capa"

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
CONF_INSTANCE_MAIL_RETENTION 	= "mail_max_retention"

# GROUP SECTION
CONF_GROUP_SECTION      	= "group"
CONF_PRINT_SEP          	= "stats_sep"
CONF_PRINT_MOB_BLESSURE 	= "stat_mob_blessure"
CONF_PRINT_MOB_NIV      	= "stat_mob_niv"
CONF_PRINT_MOB_PV       	= "stat_mob_pv"
CONF_PRINT_MOB_ATT      	= "stat_mob_att"
CONF_PRINT_MOB_ESQ      	= "stat_mob_esq"
CONF_PRINT_MOB_DEG      	= "stat_mob_deg"
CONF_PRINT_MOB_REG      	= "stat_mob_reg"
CONF_PRINT_MOB_VUE      	= "stat_mob_vue"
CONF_PRINT_MOB_MM       	= "stat_mob_mm"
CONF_PRINT_MOB_RM       	= "stat_mob_rm"
CONF_PRINT_MOB_ARM_PHY  	= "stat_mob_arm_phy"
CONF_PRINT_MOB_CAPA     	= "stat_mob_capa"
CONF_PRINT_MOB_VLC      	= "stat_mob_vlc"
CONF_PRINT_MOB_ATT_DIST 	= "stat_mob_att_dist"
CONF_PRINT_MOB_VIT      	= "stat_mob_vit"
CONF_PRINT_MOB_NB_ATT   	= "stat_mob_nb_att"
CONF_PRINT_MOB_DLA   	        = "stat_mob_dla"
CONF_PRINT_MOB_TOUR   	        = "stat_mob_tour"
CONF_PRINT_MOB_BONUS_MALUS   	= "stat_mob_bonus_malus"
CONF_PRINT_MOB_CHARGEMENT   	= "stat_mob_chargement"
CONF_PRINT_TROLL_ID   	        = "stat_troll_id"
CONF_PRINT_TROLL_RACE   	= "stat_troll_race"
CONF_PRINT_TROLL_POS    	= "stat_troll_pos"
CONF_PRINT_TROLL_DLA    	= "stat_troll_dla"
CONF_PRINT_TROLL_NIV    	= "stat_troll_niv"
CONF_PRINT_TROLL_PV     	= "stat_troll_pv"
CONF_PRINT_TROLL_ATT    	= "stat_troll_att"
CONF_PRINT_TROLL_ESQ    	= "stat_troll_esq"
CONF_PRINT_TROLL_DEG    	= "stat_troll_deg"
CONF_PRINT_TROLL_REG    	= "stat_troll_reg"
CONF_PRINT_TROLL_VUE    	= "stat_troll_vue"
CONF_PRINT_TROLL_MM     	= "stat_troll_mm"
CONF_PRINT_TROLL_RM     	= "stat_troll_rm"
CONF_PRINT_TROLL_ARM    	= "stat_troll_arm"
CONF_MOB_FULL           	= "mob_full"
CONF_MOB_FULL_INLINE           	= "mob_full_inline"
CONF_MOB_SHORT          	= "mob_short"
CONF_TROLL_FULL         	= "troll_full"
CONF_TROLL_FULL_INLINE         	= "troll_full_inline"
CONF_TROLL_SHORT        	= "troll_short"
CONF_CDM_FULL           	= "cdm_full"
CONF_CDM_SHORT          	= "cdm_short"
CONF_PIEGE_FULL           	= "piege_full"
CONF_PIEGE_SHORT          	= "piege_short"
CONF_ATT_SHORT          	= "att_short"
CONF_DEF_SHORT          	= "def_short"
CONF_CAPA_SHORT          	= "capa_short"
CONF_ATT_VT_SHORT        	= "att_vt_short"
CONF_DEF_VT_SHORT        	= "def_vt_short"
CONF_ATT_HYPNO_SHORT        	= "att_hypno_short"
CONF_DEF_HYPNO_SHORT        	= "def_hypno_short"
CONF_ATT_SACRO_SHORT        	= "att_sacro_short"
CONF_DEF_SACRO_SHORT        	= "def_sacro_short"
CONF_ATT_EXPLO_SHORT        	= "att_explo_short"
CONF_DEF_EXPLO_SHORT        	= "def_explo_short"
CONF_ATT_FULL           	= "att_full"
CONF_DEF_FULL           	= "def_full"
CONF_CAPA_FULL           	= "capa_full"
CONF_ATT_VT_FULL         	= "att_vt_full"
CONF_DEF_VT_FULL         	= "def_vt_full"
CONF_ATT_HYPNO_FULL         	= "att_hypno_full"
CONF_DEF_HYPNO_FULL         	= "def_hypno_full"
CONF_ATT_SACRO_FULL         	= "att_sacro_full"
CONF_DEF_SACRO_FULL         	= "def_sacro_full"
CONF_ATT_EXPLO_FULL         	= "att_explo_full"
CONF_DEF_EXPLO_FULL         	= "def_explo_full"






