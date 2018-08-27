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
            at.pv = max(0, int(at.pv) - int(battle.blessure))
        # Vie restante
        if battle.vie and dt:
            dt.pv = battle.vie
        # Soin
        if battle.soin and dt and dt.pv and dt.base_bonus_pv_max:
            dt.pv = min(dt.base_bonus_pv_max, int(dt.pv) + int(battle.soin))
        # PV perdus
        if battle.pv > 0 and dt and dt.pv:
            dt.pv = max(0, int(dt.pv) - int(battle.pv))
        # Fatigue (Charge)
        if battle.fatigue and at and at.fatigue is not None:
            at.fatigue = max(127, int(at.fatigue) + int(battle.fatigue))
        # Fatigue (Pouvoirs type Ronflement)
        elif battle.fatigue and dt and dt.fatigue is not None:
            dt.fatigue = max(127, int(dt.fatigue) + int(battle.fatigue))
        # Nombre d'attaque subies
        if battle.pv > 0 and dt and dt.nb_att_sub is not None:
            dt.nb_att_sub += 1
        # Stop course
        if battle.pv > 0 and dt and dt.course is not None:
            dt.course = False
        # Malus d'esquive sur attaque portée
        if battle.esq is not None and not battle.perfect_dodge and (dt or dm):
            # FIXME : problème d'affichage si une autre capa en plus de l'attaque
            # battle.capa_effet = 'ESQ -1D6'
            # battle.capa_tour = 1
            pass
        # Charger
        if battle.subtype and u"charger" in battle.subtype.lower():
            battle.subtype = battle.subtype.replace("Charger", "Charge")
        # Hypno
        if battle.subtype and battle.subtype.lower() == u"hypnotisme" and at and at.base_esq:
            dim = math.trunc(at.base_esq * 1.5) if not battle.resist else math.trunc(at.base_esq / 3)
            battle.capa_effet = 'ESQ -{}D6'.format(dim)
            battle.capa_tour = 1
        # Siphon des ames
        if battle.subtype and u"siphon" in battle.subtype.lower() and hasattr(battle, 'siphon'):
            battle.capa_effet = 'ATT -{}'.format(battle.siphon)
            battle.capa_tour = 1 if battle.resist else 2
        # Rafale psychique
        if battle.subtype and u"rafale" in battle.subtype.lower() and hasattr(battle, 'rafale'):
            battle.capa_effet = 'REG -{}'.format(battle.rafale)
            battle.capa_tour = 1 if battle.resist else 2
        return battle
