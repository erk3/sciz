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
            self.battle_event_short = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_BATTLE_EVENT_SHORT)
            self.battle_event_full = self.config.get(sg.CONF_PRINT_SECTION, sg.CONF_BATTLE_EVENT_FULL)
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
        if event.att_troll:
            event.att_entity = event.att_troll
            if event.att_troll.user:
                event.s_att_nom = event.att_troll.user.pseudo + ' (' + str(event.att_troll.id) + ')'
            else:
                event.s_att_nom = event.att_troll.nom + ' (' + str(event.att_troll.id) + ')'
        else:
            event.att_entity = event.att_mob
            event.s_att_nom = event.att_mob.nom + ' [' + event.att_mob.age + '] (' + str(event.att_mob.id) + ')'
        if event.def_troll:
            event.def_entity = event.def_troll
            if event.def_troll.user:
                event.s_def_nom = event.def_troll.user.pseudo + ' (' + str(event.def_troll.id) + ')'
            else:
                event.s_def_nom = event.def_troll.nom + ' (' + str(event.def_troll.id) + ')'
        else:
            event.def_entity = event.def_mob
            event.s_def_nom = event.def_mob.nom + ' [' + event.def_mob.age + '] (' + str(event.def_mob.id) + ')'

        event.s_pv = event.pv if event.pv != None else 0
        event.s_def_stats = ''
        event.s_def_stats += ' esq ' + str(event.esq) if event.esq else ''
        event.s_def_stats += ' sr ' + str(event.sr) if event.sr else ''
        event.s_att_stats = ''
        event.s_att_stats += ' att ' + str(event.att) if event.att else ''
        event.s_att_stats += ' deg ' + str(event.deg) if event.deg else ''
        event.s_type = event.type
        event.s_type += ' ' + event.subtype if event.subtype else ''
        if short:
            return '@' + sg.format_time(event.time) + ' : ' + self.battle_event_short.format(o=event)
        else:
            return '@' + sg.format_time(event.time) + ' : ' + self.battle_event_full.format(o=event)

    def __pprint_mob(self, mob, short):
        if mob.vit_dep: # arbitrary (any stats from cdm>=3)
            mob.comp_niv = 3
        else:
            mob.comp_niv = 1 # or 2, does not matter
        return self.__pprint_cdm(mob, short, True)
    
    # FIXME : dirty
    def __pprint_cdm(self, cdm, short, is_mob=False):
        if short and is_mob:
            return self.mob_short.format(o=cdm)
        cdm.s_blessure = cdm.blessure if cdm.blessure != None else '?'
        cdm.s_niv = sg.str_min_max(cdm.niv_min, cdm.niv_max)
        cdm.s_pv = sg.str_min_max(cdm.pv_min, cdm.pv_max)
        cdm.s_att = sg.str_min_max(cdm.att_min, cdm.att_max)
        cdm.s_esq = sg.str_min_max(cdm.esq_min, cdm.esq_max)
        cdm.s_deg = sg.str_min_max(cdm.deg_min, cdm.deg_max)
        cdm.s_reg = sg.str_min_max(cdm.reg_min, cdm.reg_max)
        cdm.s_vue = sg.str_min_max(cdm.vue_min, cdm.vue_max)
        cdm.s_arm_phy = sg.str_min_max(cdm.arm_phy_min, cdm.arm_phy_max)
        cdm.s_mm = sg.str_min_max(cdm.mm_min, cdm.mm_max)
        cdm.s_rm = sg.str_min_max(cdm.rm_min, cdm.rm_max)
        if cdm.capa_tour:
            cdm.s_capa = cdm.capa_desc + ' (' + cdm.capa_effet + ') ' + str(cdm.capa_tour) + 'T'
        cdm.s_vlc = 'Oui' if cdm.vlc else 'Non'
        cdm.s_att_dist = 'Oui' if cdm.att_dist else 'Non'
        cdm.s_vit = cdm.vit_dep
        cdm.s_nb_att_tour = cdm.nb_att_tour
            
        stats = []
        if cdm.s_niv != None: # just in case is_mob=true and no cdm
            stats = [self.niv, self.pv, self.att, self.esq, self.deg, self.reg, self.vue, self.arm_phy]
        if cdm.capa_desc != None:
            stats.append(self.capa)
        if int(cdm.comp_niv) > 2 :
            stats.extend([self.mm, self.rm, self.vlc, self.att_dist, self.vit, self.nb_att])
            
        if short:
            return '@' + sg.format_time(cdm.time) + ' : ' + self.cdm_short.format(o=cdm)
        else:
            if len(stats) > 0:
                #cdm.s_stats = (" " + self.sep + " ").join(stats)
                cdm.s_stats = ("\n").join(stats)
                cdm.s_stats = cdm.s_stats.format(o=cdm)
            else:
                return self.mob_short.format(o=cdm)
            if is_mob:
                return self.mob_full.format(o=cdm)
            else:
                return self.cdm_full.format(o=cdm)
