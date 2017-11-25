#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import ConfigParser
from classes.troll import TROLL
from classes.cdm import CDM
from classes.mob import MOB
from classes.battle import BATTLE
from classes.piege import PIEGE
import modules.globals as sg

## PrettyPrinter class for SCIZ
class PrettyPrinter:

    # Constructor
    def __init__(self):
        self.check_conf()
    
    # Configuration loader and checker
    def check_conf(self):
        try:
            # Load Mail conf
            self.troll_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_TROLL_FULL)
            self.troll_full_inline = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_TROLL_FULL_INLINE)
            self.troll_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_TROLL_SHORT)
            self.mob_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_MOB_FULL)
            self.mob_full_inline = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_MOB_FULL_INLINE)
            self.mob_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_MOB_SHORT)
            self.cdm_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_CDM_FULL)
            self.cdm_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_CDM_SHORT)
            self.piege_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PIEGE_FULL)
            self.piege_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PIEGE_SHORT)
            self.att_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_ATT_SHORT)
            self.def_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_DEF_SHORT)
            self.capa_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_CAPA_SHORT)
            self.att_fa_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_ATT_FA_SHORT)
            self.def_fa_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_DEF_FA_SHORT)
            self.att_vt_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_ATT_VT_SHORT)
            self.def_vt_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_DEF_VT_SHORT)
            self.att_hypno_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_ATT_HYPNO_SHORT)
            self.def_hypno_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_DEF_HYPNO_SHORT)
            self.att_sacro_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_ATT_SACRO_SHORT)
            self.def_sacro_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_DEF_SACRO_SHORT)
            self.att_explo_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_ATT_EXPLO_SHORT)
            self.def_explo_short = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_DEF_EXPLO_SHORT)
            self.att_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_ATT_FULL)
            self.def_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_DEF_FULL)
            self.capa_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_CAPA_FULL)
            self.att_fa_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_ATT_FA_FULL)
            self.def_fa_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_DEF_FA_FULL)
            self.att_vt_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_ATT_VT_FULL)
            self.def_vt_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_DEF_VT_FULL)
            self.att_hypno_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_ATT_HYPNO_FULL)
            self.def_hypno_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_DEF_HYPNO_FULL)
            self.att_sacro_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_ATT_SACRO_FULL)
            self.def_sacro_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_DEF_SACRO_FULL)
            self.att_explo_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_ATT_EXPLO_FULL)
            self.def_explo_full = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_DEF_EXPLO_FULL)
            self.sep = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_SEP)
            self.mob_blessure = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_BLESSURE)
            self.mob_niv = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_NIV)
            self.mob_pv = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_PV)
            self.mob_att = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_ATT)
            self.mob_esq = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_ESQ)
            self.mob_deg = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_DEG)
            self.mob_reg = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_REG)
            self.mob_vue = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_VUE)
            self.mob_mm = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_MM)
            self.mob_rm = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_RM)
            self.mob_arm_phy = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_ARM_PHY)
            self.mob_capa = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_CAPA)
            self.mob_vlc = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_VLC)
            self.mob_att_dist = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_ATT_DIST)
            self.mob_vit = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_VIT)
            self.mob_nb_att = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_NB_ATT)
            self.mob_dla = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_DLA)
            self.mob_tour = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_TOUR)
            self.mob_chargement = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_CHARGEMENT)
            self.mob_bonus_malus = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_MOB_BONUS_MALUS)
            self.troll_id = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_ID)
            self.troll_race = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_RACE)
            self.troll_niv = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_NIV)
            self.troll_pos = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_POS)
            self.troll_dla = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_DLA)
            self.troll_pv = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_PV)
            self.troll_att = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_ATT)
            self.troll_esq = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_ESQ)
            self.troll_deg = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_DEG)
            self.troll_reg = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_REG)
            self.troll_vue = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_VUE)
            self.troll_mm = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_MM)
            self.troll_rm = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_RM)
            self.troll_arm = sg.config.get(sg.CONF_GROUP_SECTION, sg.CONF_PRINT_TROLL_ARM)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise

    # Dispatcher
    def pretty_print(self, obj, short, attrs=None):
        if isinstance(obj, CDM):
            return self.__pprint_cdm(obj, short).encode(sg.DEFAULT_CHARSET)
        if isinstance(obj, PIEGE):
            return self.__pprint_piege(obj, short).encode(sg.DEFAULT_CHARSET)
        if isinstance(obj, MOB):
            return self.__pprint_mob(obj, short, attrs).encode(sg.DEFAULT_CHARSET)
        if isinstance(obj, BATTLE):
            return self.__pprint_battle(obj, short).encode(sg.DEFAULT_CHARSET)
        if isinstance(obj, TROLL):
            return self.__pprint_troll(obj, short, attrs).encode(sg.DEFAULT_CHARSET)

    def __pprint_battle(self, event, short):
        event.stringify()
        format_str = None
        format_str = self.att_short if short and (event.flag_type == 'ATT') else format_str
        format_str = self.def_short if short and (event.flag_type == 'DEF') else format_str
        format_str = self.capa_short if short and (event.flag_type == 'DEF CAPA') else format_str
        format_str = self.att_hypno_short if short and (event.flag_type == 'ATT HYPNO') else format_str
        format_str = self.def_hypno_short if short and (event.flag_type == 'DEF HYPNO') else format_str
        format_str = self.att_sacro_short if short and (event.flag_type == 'ATT SACRO') else format_str
        format_str = self.def_sacro_short if short and (event.flag_type == 'DEF SACRO') else format_str
        format_str = self.att_explo_short if short and (event.flag_type == 'ATT EXPLO') else format_str
        format_str = self.def_explo_short if short and (event.flag_type == 'DEF EXPLO') else format_str
        format_str = self.att_vt_short if short and (event.flag_type == 'ATT VT') else format_str
        format_str = self.def_vt_short if short and (event.flag_type == 'DEF VT') else format_str
        format_str = self.att_fa_short if short and (event.flag_type == 'ATT FA') else format_str
        format_str = self.def_fa_short if short and (event.flag_type == 'DEF FA') else format_str
        format_str = self.att_full if not short and (event.flag_type == 'ATT') else format_str
        format_str = self.def_full if not short and (event.flag_type == 'DEF') else format_str
        format_str = self.capa_full if not short and (event.flag_type == 'DEF CAPA') else format_str
        format_str = self.att_hypno_full if not short and (event.flag_type == 'ATT HYPNO') else format_str
        format_str = self.def_hypno_full if not short and (event.flag_type == 'DEF HYPNO') else format_str
        format_str = self.att_sacro_full if not short and (event.flag_type == 'ATT SACRO') else format_str
        format_str = self.def_sacro_full if not short and (event.flag_type == 'DEF SACRO') else format_str
        format_str = self.att_explo_full if not short and (event.flag_type == 'ATT EXPLO') else format_str
        format_str = self.def_explo_full if not short and (event.flag_type == 'DEF EXPLO') else format_str
        format_str = self.att_vt_full if not short and (event.flag_type == 'ATT VT') else format_str
        format_str = self.def_vt_full if not short and (event.flag_type == 'DEF VT') else format_str
        format_str = self.att_fa_full if not short and (event.flag_type == 'ATT FA') else format_str
        format_str = self.def_fa_full if not short and (event.flag_type == 'DEF FA') else format_str
        if format_str != None:
            return '@' + sg.format_time(event.time) + ' ' + format_str.format(o=event)
        else:
            return '' # Should never happen

    def __pprint_mob(self, mob, short, attrs):
        # Generate the string representation
        mob.stringify()
        if short:
            return self.mob_short.format(o=mob)
        else:
            # Select the attributes printable
            stats = []
            if mob.niv_min or mob.niv_max: # At least one CDM
                stats = [self.mob_blessure, self.mob_niv, self.mob_pv, self.mob_att, self.mob_esq, self.mob_deg, self.mob_reg, self.mob_vue, self.mob_arm_phy]
            if mob.capa_desc != None:
                stats.append(self.mob_capa)
            if mob.vit_dep != None : #Arbitrary, any stats from CDM>=3 
                stats.extend([self.mob_mm, self.mob_rm, self.mob_vlc, self.mob_att_dist, self.mob_vit, self.mob_nb_att])
            if mob.dla != None : #Arbitrary, any stats from CDM>=4
                stats.extend([self.mob_dla, self.mob_tour, self.mob_chargement, self.mob_bonus_malus])
            # Filter out not wanted attributes
            stats_filtered = []
            if attrs:
                for attr in attrs:
                    try:
                        val = getattr(self, 'mob_' + attr)
                        if val in stats:
                            stats_filtered.append(val)
                    except:
                        pass
            stats = stats_filtered if len(stats_filtered) > 0 else stats
            # Format
            if len(stats) < 1:
                return ''
            elif attrs == None or len(attrs) > 1:
                sep = "\n"
                mob.s_stats = sep + (sep).join(stats)
                mob.s_stats = mob.s_stats.format(o=mob)
                return self.mob_full.format(o=mob)
            else:
                sep = " "
                mob.s_stats = sep + (sep).join(stats)
                mob.s_stats = mob.s_stats.format(o=mob)
                return self.mob_full_inline.format(o=mob)
    
    def __pprint_piege(self, piege, short):
        # Generate the string representation
        piege.stringify()
        format_str = self.piege_short if short else self.piege_full
        return '@' + sg.format_time(piege.time) + ' ' + format_str.format(o=piege)
    
    def __pprint_cdm(self, cdm, short):
        # Generate the string representation
        cdm.stringify()
        if short:
            return '@' + sg.format_time(cdm.time) + ' ' + self.cdm_short.format(o=cdm)
        else:
            # Select the attributes printable
            stats = [self.mob_blessure, self.mob_niv, self.mob_pv, self.mob_att, self.mob_esq, self.mob_deg, self.mob_reg, self.mob_vue, self.mob_arm_phy]
            if cdm.capa_desc != None:
                stats.append(self.mob_capa)
            if int(cdm.comp_niv) > 2 : 
                stats.extend([self.mob_mm, self.mob_rm, self.mob_vlc, self.mob_att_dist, self.mob_vit, self.mob_nb_att])
            if int(cdm.comp_niv) > 3 : 
                stats.extend([self.mob_dla, self.mob_tour, self.mob_chargement, self.mob_bonus_malus])
            # Format
            if len(stats) < 1:
                return ''
            else:
                sep = "\n"
                cdm.s_stats = sep + (sep).join(stats)
                cdm.s_stats = cdm.s_stats.format(o=cdm)
                return self.cdm_full.format(o=cdm)

    def __pprint_troll(self, troll, short, attrs):
        # Generate the string representation
        try:
            troll.stringify()
        except Exception:
            return ''
        if short:
            return self.troll_short.format(o=troll)
        else:
            # Select the attributes printable
            stats = [self.troll_id]
            if troll.niv != None: # Any attr retrieved from FTP call
                stats.extend([self.troll_race, self.troll_niv])
            if troll.pv != None: # Any attr retrieved from SP call
                stats.extend([self.troll_pos, self.troll_dla, self.troll_pv, self.troll_att, self.troll_esq, self.troll_deg, self.troll_reg, self.troll_vue, self.troll_arm, self.troll_mm, self.troll_rm])
            # Filter out not wanted attributes
            stats_filtered = []
            if attrs:
                for attr in attrs:
                    try:
                        val = getattr(self, 'troll_' + attr)
                        if val in stats:
                            stats_filtered.append(val)
                    except:
                        pass
                stats = stats_filtered
            # Format
            if len(stats) < 1:
                return ''
            elif attrs == None or len(attrs) > 1:
                sep = "\n"
                troll.s_stats = sep + (sep).join(stats)
                troll.s_stats = troll.s_stats.format(o=troll)
                return self.troll_full.format(o=troll)
            else:
                sep = " "
                troll.s_stats = sep + (sep).join(stats)
                troll.s_stats = troll.s_stats.format(o=troll)
                return self.troll_full_inline.format(o=troll)
