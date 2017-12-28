#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import ConfigParser, math
from classes.battle import BATTLE
import modules.globals as sg

## GameEngine class for SCIZ
class GameEngine:

    # Constructor
    def __init__(self):
        self.check_conf()
        
    # Configuration loader and checker
    def check_conf(self):
        pass

    # Play any object (dispatcher)
    def play(self, obj):
        if isinstance(obj, BATTLE):
            return self.__play_battle(obj)
        return None

    # Play battle
    def __play_battle(self, battle):
        # Shortcuts
        at = battle.att_troll
        dt = battle.def_troll
        am = battle.att_mob
        dm = battle.def_mob
        # Blessure
        if battle.blessure and at and at.pv:
            at.pv = max(0, at.pv - int(battle.blessure))
        # Vie restante
        if battle.vie and dt:
            dt.pv = battle.vie
        # Soin
        if battle.soin and dt and dt.pv and dt.base_bonus_pv_max:
            dt.pv = min(dt.base_bonus_pv_max, dt.pv + int(battle.soin))
        # PV perdus
        if battle.pv and dt and dt.pv:
            dt.pv = max(0, dt.pv - int(battle.pv))
        # Hypno
        if battle.subtype and battle.subtype.lower() == "hypnotisme" and at and at.base_esq:
            dim = math.trunc(at.base_esq * 1.5) if not battle.resist else math.trunc(at.base_esq / 3)
            battle.capa_effet = 'ESQ -{}D6'.format(dim)
            battle.capa_tour = 1
        return battle
