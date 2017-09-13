#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import ConfigParser
from classes.troll import TROLL
from classes.cdm import CDM
from classes.mob import MOB
from classes.battle_event import BATTLE_EVENT
import modules.globals as sg

## PrettyPrinter class for SCIZ
class PrettyPrinter:

    # Constructor
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.check_conf()
    
    # Configuration loader and checker
    def check_conf(self):
        try:
            # Load Mail conf
            self.troll_full = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_TROLL_FULL)
            self.troll_short = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_TROLL_SHORT)
            self.mob_full = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_MOB_FULL)
            self.mob_short = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_MOB_SHORT)
            self.cdm_full = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_CDM_FULL)
            self.cdm_short = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_CDM_SHORT)
            self.att_short = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_ATT_SHORT)
            self.def_short = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_DEF_SHORT)
            self.hypno_short = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_HYPNO_SHORT)
            self.att_full = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_ATT_FULL)
            self.def_full = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_DEF_FULL)
            self.hypno_full = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_HYPNO_FULL)
            self.sep = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_SEP)
            self.mob_blessure = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_BLESSURE)
            self.mob_niv = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_NIV)
            self.mob_pv = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_PV)
            self.mob_att = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_ATT)
            self.mob_esq = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_ESQ)
            self.mob_deg = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_DEG)
            self.mob_reg = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_REG)
            self.mob_vue = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_VUE)
            self.mob_mm = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_MM)
            self.mob_rm = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_RM)
            self.mob_arm_phy = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_ARM_PHY)
            self.mob_capa = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_CAPA)
            self.mob_vlc = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_VLC)
            self.mob_att_dist = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_ATT_DIST)
            self.mob_vit = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_VIT)
            self.mob_nb_att = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MOB_NB_ATT)
            self.troll_race = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_RACE)
            self.troll_niv = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_NIV)
            self.troll_pos = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_POS)
            self.troll_dla = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_DLA)
            self.troll_pv = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_PV)
            self.troll_att = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_ATT)
            self.troll_esq = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_ESQ)
            self.troll_deg = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_DEG)
            self.troll_reg = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_REG)
            self.troll_vue = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_VUE)
            self.troll_mm = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_MM)
            self.troll_rm = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_RM)
            self.troll_arm = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_TROLL_ARM)
        except ConfigParser.Error as e:
            e.sciz_logger_flag = True
            self.logger.error("Fail to load config! (ConfigParser error:" + str(e) + ")")
            raise

    # Dispatcher
    def pretty_print(self, obj, short, attrs=None):
        if isinstance(obj, CDM):
            return self.__pprint_cdm(obj, short).encode(sg.DEFAULT_CHARSET)
        if isinstance(obj, MOB):
            return self.__pprint_mob(obj, short, attrs).encode(sg.DEFAULT_CHARSET)
        if isinstance(obj, BATTLE_EVENT):
            return self.__pprint_battle_event(obj, short).encode(sg.DEFAULT_CHARSET)
        if isinstance(obj, TROLL):
            return self.__pprint_troll(obj, short, attrs).encode(sg.DEFAULT_CHARSET)

    def __pprint_battle_event(self, event, short):
        event.stringify()
        format_str = None
        format_str = self.att_short if short and (event.flag_type == 'ATT') else format_str
        format_str = self.def_short if short and (event.flag_type == 'DEF') else format_str
        format_str = self.hypno_short if short and (event.flag_type == 'HYPNO') else format_str
        format_str = self.att_full if not short and (event.flag_type == 'ATT') else format_str
        format_str = self.def_full if not short and (event.flag_type == 'DEF') else format_str
        format_str = self.hypno_full if not short and (event.flag_type == 'HYPNO') else format_str
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
            mob.s_stats = ("\n").join(stats)
            mob.s_stats = mob.s_stats.format(o=mob)
            return self.mob_full.format(o=mob)
    
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
            # Format
            cdm.s_stats = ("\n").join(stats)
            cdm.s_stats = cdm.s_stats.format(o=cdm)
            return self.cdm_full.format(o=cdm)

    def __pprint_troll(self, troll, short, attrs):
        # Generate the string representation
        troll.stringify()
        if short:
            return self.troll_short.format(o=troll)
        else:
            # Select the attributes printable
            stats = []
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
            troll.s_stats = ("\n").join(stats)
            troll.s_stats = troll.s_stats.format(o=troll)
            return self.troll_full.format(o=troll)

