#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
#from __future__ import unicode_literals
import ConfigParser
from classes.cdm import CDM
from classes.mob import MOB
from classes.battle_event import BATTLE_EVENT
import modules.globals as sg

## PrettyPrinter class for SCIZ
class PrettyPrinter:

    # Constructor
    def __init__(self, config):
        self.config = config
        self.check_conf()
    
    # Configuration loader and checker
    def check_conf(self):
        try:
            # Load Mail conf
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
            self.niv = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_NIV)
            self.pv = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_PV)
            self.att = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_ATT)
            self.esq = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_ESQ)
            self.deg = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_DEG)
            self.reg = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_REG)
            self.vue = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_VUE)
            self.mm = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_MM)
            self.rm = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_RM)
            self.arm_phy = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_ARM_PHY)
            self.capa = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_CAPA)
            self.vlc = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_VLC)
            self.att_dist = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_ATT_DIST)
            self.vit = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_VIT)
            self.nb_att = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_PRINT_NB_ATT)
        except ConfigParser.Error as e:
            print("Fail to load config! (ConfigParser error:" + str(e) + ")")
            raise

    # Dispatcher
    def pretty_print(self, obj, short):
        if isinstance(obj, CDM):
            return self.__pprint_cdm(obj, short).encode(sg.DEFAULT_CHARSET)
        if isinstance(obj, MOB):
            return self.__pprint_mob(obj, short).encode(sg.DEFAULT_CHARSET)
        if isinstance(obj, BATTLE_EVENT):
            return self.__pprint_battle_event(obj, short).encode(sg.DEFAULT_CHARSET)

    def __pprint_battle_event(self, event, short):
        event.stringify()
        format_str = None
        format_str = self.att_short if short and (event.s_flag_type == 'ATT') else format_str
        format_str = self.def_short if short and (event.s_flag_type == 'DEF') else format_str
        format_str = self.hypno_short if short and (event.s_flag_type == 'HYPNO') else format_str
        format_str = self.att_full if not short and (event.s_flag_type == 'ATT') else format_str
        format_str = self.def_full if not short and (event.s_flag_type == 'DEF') else format_str
        format_str = self.hypno_full if not short and (event.s_flag_type == 'HYPNO') else format_str
        if format_str != None:
            return '@' + sg.format_time(event.time) + ' : ' + format_str.format(o=event)
        else:
            return '' # Should never happen

    def __pprint_mob(self, mob, short):
        # Generate the string representation
        mob.stringify()
        if short:
            return self.mob_short.format(o=mob)
        else:
            # Select the attributes printable
            stats = []
            if mob.niv_min or mob.niv_max: # At least one CDM
                stats = [self.niv, self.pv, self.att, self.esq, self.deg, self.reg, self.vue, self.arm_phy]
            if mob.capa_desc != None:
                stats.append(self.capa)
            if mob.vit_dep != None : #Arbitrary, any stats from CDM>=3 
                stats.extend([self.mm, self.rm, self.vlc, self.att_dist, self.vit, self.nb_att])
            mob.s_stats = ("\n").join(stats)
            mob.s_stats = mob.s_stats.format(o=mob)
            return self.mob_full.format(o=mob)
    
    def __pprint_cdm(self, cdm, short):
        # Generate the string representation
        cdm.stringify()
        if short:
            return '@' + sg.format_time(cdm.time) + ' : ' + self.cdm_short.format(o=cdm)
        else:
            # Select the attributes printable
            stats = [self.niv, self.pv, self.att, self.esq, self.deg, self.reg, self.vue, self.arm_phy]
            if cdm.capa_desc != None:
                stats.append(self.capa)
            if int(cdm.comp_niv) > 2 : 
                stats.extend([self.mm, self.rm, self.vlc, self.att_dist, self.vit, self.nb_att])

            cdm.s_stats = ("\n").join(stats)
            cdm.s_stats = cdm.s_stats.format(o=cdm)
            return self.cdm_full.format(o=cdm)

