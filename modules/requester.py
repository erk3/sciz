#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.being_troll_private import TrollPrivate
from classes.being_mob_private import MobPrivate
from classes.tresor_private import TresorPrivate
from classes.champi_private import ChampiPrivate
from classes.lieu_piege import Piege
from classes.event import Event
from classes.event_cdm import cdmEvent
from classes.event_aa import aaEvent
from classes.event_battle import battleEvent
from classes.lieu import Lieu
from classes.user import User
from classes.being_mob import Mob
from modules.sql_helper import unaccent
from sqlalchemy import and_, or_, func, case
from statistics import mean
import re, datetime, dateutil.relativedelta
import modules.globals as sg


# CLASS DEFINITION
class Requester:

    # Consts
    mod_keywords = ['filter']
    int_keywords = ['id', 'niv', 'x', 'y', 'n', 'select']
    str_keywords = {'troll': TrollPrivate, 'event': Event,
                    'bestiaire': cdmEvent, 'recherche': MobPrivate, 'mob': MobPrivate, 'recap': MobPrivate,
                    'tresor': TresorPrivate, 'champi': ChampiPrivate, 'lieu': Lieu}

    # Constructor
    def __init__(self):
        self.check_conf()

    # Configuration loader and checker
    def check_conf(self):
        # No conf needed yet
        pass

    # Request
    def request(self, coterie_or_user, search):
        return ['Une chauve-souris hors-service revient vers vous...']
        search = search.lower()
        # Special coterie handling
        if '%coterie' in search:
            search = search.replace('%coterie', '%troll')
            members_list = coterie_or_user.members_list_sharing()
            search += ' %id:' + ','.join([str(member) for member in members_list])
            search += ' %select:' + str(len(members_list))
        # Parse the keywords
        args = {}
        matchall = re.finditer(r'%(?P<type>\w+)(:(?P<subtype>(\d|\w|,|_|-)+))?', search)
        for match in matchall:
            type = match.groupdict()['type']
            type = sg.flatten(type)
            if type not in self.str_keywords and type not in self.int_keywords + self.mod_keywords:
                continue
            subtypes = match.groupdict()['subtype']
            subtypes = [subtype for subtype in subtypes.split(',') if subtype != ''] if subtypes is not None else []
            if type in self.int_keywords:
                i = 0
                while i < len(subtypes):
                    if subtypes[i].count('_') == 1:
                        subtypes[i] = subtypes[i].split('_')
                        try:
                            subtypes[i] = sorted(list(map(lambda x: int(x), subtypes[i])))
                        except Exception as e:
                            subtypes[i] = []
                    else:
                        try:
                            subtypes[i] = int(subtypes[i])
                        except Exception as e:
                            del subtypes[i]
                    i += 1
                if any(x is not None for x in subtypes):
                    if type not in args or args[type] is None:
                        args[type] = subtypes
                    else:
                        args[type] = args[type] + subtypes
            else:
                if type not in args or args[type] is None:
                    args[type] = subtypes
                else:
                    args[type] = args[type] + subtypes
        # MP/PX handle
        if args == {}:
            if '%px' in search:
                return [coterie_or_user.px_link]
            if '%mp' in search:
                return [coterie_or_user.mp_link]
            if 'help' in search:
                return [sg.conf[sg.CONF_SCIZ_HELP]]
        # Build the query
        res = []
        for k in self.str_keywords:
            if k in args:
                # Get the viewers and query
                if k in ['recherche', 'bestiaire']:
                    query = self.requester_build_query(k, self.str_keywords[k], [], [], args)
                elif k in ['event']:
                    users_id = coterie_or_user.members_list_sharing(None, None, True) # Don't get events of people not sharing them
                    query = self.requester_build_query(k, self.str_keywords[k], users_id, [], args)
                else:
                    # Remember here that reconciliation happened before
                    sp4_users_id = coterie_or_user.members_list_sharing(True, True, True)
                    users_id = coterie_or_user.members_list_sharing(False, True, True)
                    if len(users_id) < 1:
                        sp4_users_id = coterie_or_user.members_list_sharing(True, None, True)
                        users_id = coterie_or_user.members_list_sharing(False, None, True)
                    if len(users_id) < 1:
                        sp4_users_id = coterie_or_user.members_list_sharing(True, True, None)
                        users_id = coterie_or_user.members_list_sharing(False, True, None)
                    if k == 'troll':
                        query = self.requester_build_query(k, self.str_keywords[k], users_id, sp4_users_id, args)
                    else:
                        query = self.requester_build_query(k, self.str_keywords[k], users_id + sp4_users_id, [], args)
                # Query
                if query is not None:
                    q = query.all()
                    for r in q:
                        s = None
                        if k == 'recap':
                            s = self.recap(r, users_id + sp4_users_id)
                        elif k == 'recherche':
                            sg.zero_out_but(r, ['mob_id', 'pos_x', 'pos_y', 'pos_n', 'last_seen_at'])
                            s = sg.no.stringify(r)
                        else:
                            if k == 'bestiaire':
                                r = self.bestiaire(r)
                            s = sg.no.stringify(r, None, args['filter'] if 'filter' in args else None)
                        if s is not None and s != '':
                            res.append(s)
        if len(res) < 1:
            return ['Une chauve-souris l\'air bredouille et désemparée revient vers vous...']
        return res

    @staticmethod
    def requester_build_query(key, cls, users_id, sp4_users_id, args):
        # Setup
        offset, limit = None, 1
        query = sg.db.session.query(cls)
        # Attrs
        attr_id = 'id'
        if cls is Event or cls is cdmEvent:
            attr_id = 'owner_id'
        elif hasattr(cls, key + '_id'):
            attr_id = key + '_id'
        elif key in ['recherche', 'recap']:
            attr_id = 'mob_id'
        attr_niv_min = 'niv' if hasattr(cls, 'niv') else 'niv_min'
        attr_niv_max = 'niv' if hasattr(cls, 'niv') else 'niv_max'
        attr_pos_x, attr_pos_y, attr_pos_n = 'pos_x', 'pos_y', 'pos_n'
        # Class filters and query adjustements
        if cls is Event:
            filters = cls.owner_id.in_(users_id)
        elif cls is cdmEvent:
            query = query.outerjoin(User, cls.owner_id == User.id)
        elif cls is Lieu:
            query = query.outerjoin(Piege)
            filters = and_(cls.destroyed != True, or_(cls.owner_id is None, cls.owner_id.in_(users_id)))
        else:
            # Privates
            query = query.distinct(getattr(cls, attr_id))
            if key == 'recherche':
                query = query.outerjoin(User, cls.viewer_id == User.id)
            elif cls is TresorPrivate:
                query = query.join(cls.tresor_meta)
            elif cls is TrollPrivate:
                query = query.join(cls.troll)
            elif cls is MobPrivate:
                query = query.join(cls.mob)
            if key == 'recherche':
                filters = and_(getattr(cls.mob.property.mapper.class_, 'mort') == False, getattr(cls, attr_pos_x) is not None, getattr(cls, attr_pos_y) is not None, getattr(cls, attr_pos_n) is not None)
            if key == 'troll':
                # Exclude personnal private for those not sharing it
                filters = case([(cls.viewer_id.in_(users_id), and_(cls.viewer_id.in_(users_id), cls.troll_id != cls.viewer_id))], else_= cls.viewer_id.in_(sp4_users_id))
            else:
                filters = cls.viewer_id.in_(users_id)
        # Dynamic build filters
        for k in args:
            tmp_filter = None
            for v in args[k]:
                sub_tmp_filter = None
                # INT keys
                if k == 'id':
                    if isinstance(v, list):
                        sub_tmp_filter = and_(getattr(cls, attr_id) >= v[0], getattr(cls, attr_id) <= v[1])
                    else:
                        sub_tmp_filter = getattr(cls, attr_id) == v
                elif k == 'niv' and cls not in [Event, Lieu]:
                    if isinstance(v, list):
                        sub_tmp_filter = and_(getattr(cls, attr_niv_min) >= v[0], getattr(cls, attr_niv_max) <= v[1])
                    else:
                        sub_tmp_filter = and_(getattr(cls, attr_niv_min) >= v, getattr(cls, attr_niv_max) <= v)
                elif k == 'x':
                    if isinstance(v, list):
                        sub_tmp_filter = and_(getattr(cls, attr_pos_x) >= v[0], getattr(cls, attr_pos_x) <= v[1])
                    else:
                        sub_tmp_filter = and_(getattr(cls, attr_pos_x) >= v, getattr(cls, attr_pos_x) <= v)
                elif k == 'y':
                    if isinstance(v, list):
                        sub_tmp_filter = and_(getattr(cls, attr_pos_y) >= v[0], getattr(cls, attr_pos_y) <= v[1])
                    else:
                        sub_tmp_filter = and_(getattr(cls, attr_pos_y) >= v, getattr(cls, attr_pos_y) <= v)
                elif k == 'n':
                    if isinstance(v, list):
                        sub_tmp_filter = and_(getattr(cls, attr_pos_n) >= v[0], getattr(cls, attr_pos_n) <= v[1])
                    else:
                        sub_tmp_filter = and_(getattr(cls, attr_pos_n) >= v, getattr(cls, attr_pos_n) <= v)
                # Special select modifier
                elif k == 'select':
                    if isinstance(v, list):
                        offset = max(v[0] - 1, 0)
                        limit = max(min(v[1] - offset, 10), 1)
                    else:
                        limit = max(min(v, 10), 1)
                # STR keys
                elif k == key:
                    # Remove accented chars
                    v = sg.flatten(v)
                    if k == 'event':
                        sub_tmp_filter = or_(unaccent(getattr(cls, 'mail_subject')).ilike('%' + v + '%'),
                                             unaccent(getattr(cls, 'mail_body')).ilike('%' + v + '%'))
                    elif k == 'lieu':
                        sub_tmp_filter = unaccent(getattr(cls, 'nom')).ilike('%' + v + '%')
                    elif k == 'champi':
                        sub_tmp_filter = or_(unaccent(getattr(cls, 'nom')).ilike('%' + v + '%'),
                                             unaccent(getattr(cls, 'qualite')).ilike('%' + v + '%'))
                    elif k == 'tresor':
                        sub_tmp_filter = or_(unaccent(getattr(cls, 'nom')).ilike('%' + v + '%'),
                                             unaccent(getattr(cls, 'templates')).ilike('%' + v + '%'),
                                             unaccent(getattr(cls.tresor_meta.property.mapper.class_, 'type')).ilike('%' + v + '%'))
                    elif k == 'troll':
                        sub_tmp_filter = or_(unaccent(getattr(cls.troll.property.mapper.class_, 'nom')).ilike('%' + v + '%'),
                                             unaccent(getattr(cls.troll.property.mapper.class_, 'race')).ilike('%' + v + '%'))
                    elif k in ['mob', 'recap']:
                        sub_tmp_filter = or_(unaccent(getattr(cls.mob.property.mapper.class_, 'nom')).ilike('%' + v + '%'),
                                             unaccent(getattr(cls.mob.property.mapper.class_, 'tag')).ilike('%' + v + '%'),
                                             unaccent(getattr(cls.mob.property.mapper.class_, 'age')).ilike('%' + v + '%'),
                                             unaccent(getattr(cls.mob.property.mapper.class_, 'race')).ilike('%' + v + '%'))
                    elif k == 'recherche':
                        sub_tmp_filter = or_(unaccent(getattr(cls.mob.property.mapper.class_, 'nom')).ilike('%' + v + '%'),
                                             unaccent(getattr(cls.mob.property.mapper.class_, 'age')).ilike('%' + v + '%'),
                                             unaccent(getattr(cls.mob.property.mapper.class_, 'race')).ilike('%' + v + '%'))
                    elif k == 'bestiaire':
                        sub_tmp_filter = or_(unaccent(getattr(cls, 'mob_nom')).ilike('%' + v + '%'),
                                             unaccent(getattr(cls, 'mob_age')).ilike('%' + v + '%'))
                if sub_tmp_filter is not None:
                    if tmp_filter is None:
                        tmp_filter = sub_tmp_filter
                    elif k == 'id':
                        tmp_filter = or_(sub_tmp_filter, tmp_filter)
                    else:
                        tmp_filter = and_(sub_tmp_filter, tmp_filter)
            if tmp_filter is not None:
                if filters is None:
                    filters = tmp_filter
                else:
                    filters = and_(tmp_filter, filters)
        if filters is not None:
            query = query.filter(filters)
        # Orders
        if cls is Event:
            query = query.order_by(cls.time.desc())
        elif cls is cdmEvent:
            offset, limit = None, 1
            query = query.order_by(func.char_length(cls.mob_nom))
        elif cls is Lieu:
            query = query.order_by(cls.last_seen_at.desc())
        elif cls is TrollPrivate:
            query = query.order_by(getattr(cls, attr_id).desc(), cls.last_event_update_at.desc().nullslast(), cls.last_sp4_update_at.desc().nullslast(), cls.last_seen_at.desc().nullslast()).subquery()
            join_cond = and_(getattr(cls, attr_id) == getattr(query.c, attr_id), cls.viewer_id == query.c.viewer_id)
            query = sg.db.session.query(cls).join(query, join_cond).order_by(cls.last_event_update_at.desc().nullslast(), cls.last_sp4_update_at.desc().nullslast(), cls.last_seen_at.desc().nullslast())
        else:
            query = query.order_by(getattr(cls, attr_id).desc(), cls.last_event_update_at.desc().nullslast(), cls.last_seen_at.desc().nullslast()).subquery()
            join_cond = and_(getattr(cls, attr_id) == getattr(query.c, attr_id), cls.viewer_id == query.c.viewer_id)
            query = sg.db.session.query(cls).join(query, join_cond).order_by(cls.last_event_update_at.desc().nullslast(), cls.last_seen_at.desc().nullslast())
        query = query.offset(offset).limit(limit)
        return query

    # Do a recap !
    @staticmethod
    def recap(o, users_id):
        # Setup
        vie_min, vie_max, blessure = o.vie_min, o.vie_max, o.blessure
        degats = 0
        replay = 0
        mort, mort_time = False, 0
        then = datetime.datetime.now() + dateutil.relativedelta.relativedelta(days=-2)
        #then = datetime.datetime.min # FOR TESTING ONLY
        last_play = then
        if isinstance(o, TrollPrivate):
            cls, attr_id, tour_min = aaEvent, 'troll_id', 9 * 60 # This is a really dummy approx, how can we do better ?
        else:
            cls, attr_id, tour_min = cdmEvent, 'mob_id', o.tour_min
        # Get last AA or CDM
        last_aa_cdm = sg.db.session.query(cls).filter(getattr(cls, attr_id) == getattr(o, attr_id), cls.owner_id.in_(users_id), cls.time > last_play).order_by(cls.time.desc()).first()
        # Get battle events
        last_play = last_aa_cdm.time if last_aa_cdm is not None else last_play
        battles = sg.db.session.query(battleEvent).filter(and_(battleEvent.owner_id.in_(users_id), battleEvent.time > last_play, or_(battleEvent.att_id == getattr(o, attr_id), battleEvent.def_id == getattr(o, attr_id)))).order_by(battleEvent.time.asc()).all()
        # Compute
        for battle in battles:
            if getattr(o, attr_id) == battle.att_id:
                elapsedTime = (battle.time - last_play).total_seconds() / 60
                # A mob play everything in one time, so one hour should be large enough
                # FIXME : how to estimate for a troll ?
                if replay == 0 or elapsedTime > 60:
                    replay += 1
                last_play = battle.time
            elif getattr(o, attr_id) == battle.def_id and battle.pv is not None:
                degats += battle.pv
                if battle.mort:
                    mort, mort_time = True, battle.time
        # Estimated reg
        reg_min, reg_max = None, None
        if hasattr(o, 'reg_min') and o.reg_min is not None:
            reg_min = o.reg_min * replay
        if hasattr(o, 'reg_max') and o.reg_max is not None:
            reg_max = o.reg_max * replay * 3
        # Estimated vie
        if vie_min is not None:
            vie_min -= degats
        if vie_max is not None:
            vie_max -= degats
        # Prettyprint
        res = o.nom_complet
        recap = ''
        if mort:
            return res + '\n' + 'Tué le ' + sg.format_time(mort_time)
        elif isinstance(o, MobPrivate) and o.mob.mort:
            return res + ' est mort il y a quelques temps...'
        if last_aa_cdm is not None and not mort:
            recap += '\n' + str(last_aa_cdm.blessure) + '% de blessure le ' + sg.format_time(last_aa_cdm.time)
        if degats > 0:
            recap += '\n' + 'Total depuis' + (' le ' + sg.format_time(then) if last_aa_cdm is None else '') + ' : -' + str(degats)
        if vie_min is not None and vie_max is not None and (len(battles) > 0 or last_aa_cdm is not None):
            recap += '\n' + 'PdV restants : ' + sg.str_min_max(max(vie_min, 1), vie_max)
        if isinstance(o, MobPrivate) and replay > 0:
            recap += '\n' + 'A rejoué au minimum ' + str(replay) + ' fois' + (' depuis le ' + sg.format_time(then) if last_aa_cdm is None else '')
        if reg_min is not None and reg_max is not None and replay > 0:
            recap += '\n' + 'PdV minimums régénérés : ' + sg.str_min_max(reg_min, reg_max)
        if recap == '':
            recap = ' s\'ennuie !'
        return res + recap

    def bestiaire(self, name, age):
        # Get all the related CdM
        res = sg.db.session.query(cdmEvent) \
            .filter(cdmEvent.mob_nom == name, cdmEvent.mob_age == age) \
            .order_by(cdmEvent.time.desc()).all()
        # Create a mob private
        pm = MobPrivate()
        pm.mob = Mob(nom=name, age=age)
        pm.mob = Mob.link_metamob(pm.mob)
        # Copy the fixed properties and compute a set of cdms regrouped by mob id
        list_of_cdm_by_mob_id = {}
        for p in res:
            sg.copy_properties(p, pm, ['capa_desc', 'capa_effet', 'capa_tour', 'capa_portee', 'nb_att_tour',
                                       'vit_dep', 'vlc', 'vole', 'att_dist', 'att_mag'], False)
            if p.mob_id in list_of_cdm_by_mob_id:
                list_of_cdm_by_mob_id[p.mob_id] = list_of_cdm_by_mob_id[p.mob_id] + [p]
            else:
                list_of_cdm_by_mob_id[p.mob_id] = [p]
        # Compute floating properties
        for attr in ['niv', 'pdv', 'att', 'esq', 'deg', 'reg', 'arm_phy', 'arm_mag', 'vue', 'mm', 'rm', 'tour']:
            attr_min = attr + '_min'
            attr_max = attr + '_max'
            aggregated_cdm_list = []
            flag_min_max = False
            # Compute real min/max for a same mob then add its final cdm to the aggregated list
            for cdm_by_mob_id in list_of_cdm_by_mob_id:
                aggregated_cdm = cdmEvent()
                list_attr_min = list(filter(None.__ne__, (getattr(cdm, attr_min) for cdm in list_of_cdm_by_mob_id[cdm_by_mob_id])))
                list_attr_max = list(filter(None.__ne__, (getattr(cdm, attr_max) for cdm in list_of_cdm_by_mob_id[cdm_by_mob_id])))
                if len(list_attr_min) > 0:
                    setattr(aggregated_cdm, attr_min, sg.do_unless_none(max, list_attr_min))
                if len(list_attr_max) > 0:
                    setattr(aggregated_cdm, attr_max, sg.do_unless_none(min, list_attr_max))
                aggregated_cdm_list.append(aggregated_cdm)
            # Compute the final value (excluding min or max only cdm if any cdm for a mob has both)
            list_attr_min = []
            list_attr_max = []
            for cdm in aggregated_cdm_list:
                _min = getattr(cdm, attr_min)
                _max = getattr(cdm, attr_max)
                if _min is not None and _max is not None:
                    flag_min_max = True
                    list_attr_min = []
                    list_attr_max = []
                if _min is not None:
                    if not flag_min_max or _max is not None:
                        list_attr_min.append(_min)
                if _max is not None:
                    if not flag_min_max or _min is not None:
                        list_attr_max.append(_max)
            if len(list_attr_min) > 0:
                setattr(pm, attr_min, min(list_attr_min))
            if len(list_attr_max) > 0:
                setattr(pm, attr_max, max(list_attr_max))
        return sg.no.stringify(pm, None, None)
