#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.event import Event
from classes.event_battle import battleEvent
from classes.event_cdm import cdmEvent
from classes.event_aa import aaEvent
from classes.event_tp import tpEvent
from classes.event_cp import cpEvent
from classes.event_tresor import tresorEvent
from classes.event_champi import champiEvent
from classes.tresor_private import TresorPrivate
from classes.champi_private import ChampiPrivate
from classes.lieu import Lieu
from classes.lieu_piege import Piege
from classes.being_troll_private import TrollPrivate
from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, UniqueConstraint, asc, or_, and_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import ReturnTypeFromArgs

import copy, requests, json, datetime
import modules.globals as sg

# CLASS DEFINITION
class Hook(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Coterie identifier
    coterie_id = Column(Integer, ForeignKey('coterie.id'))
    # Type of hook (can currently be Miaou or Discord)
    type = Column(String(50), nullable=False)
    # JWT
    jwt = Column(Text)
    # Last event pushed
    last_event_id = Column(Integer, ForeignKey('event.id', ondelete='SET NULL'))
    # JSON format
    format = Column(JSON)

    # Associations
    coterie = relationship('Coterie', back_populates='hooks', primaryjoin='Hook.coterie_id == Coterie.id')

    # SQL Table Mapping
    __tablename__ = 'hook'
    __table_args__ = (UniqueConstraint('coterie_id', 'type'), )

    # Format <=> UI Vuetify JSON (Basically composed strings as tokens array)
    @classmethod
    def format2ui(cls, f, hat=True):
        f = copy.deepcopy(f)
        for key in f:
            if (hat and any(k in key for k in ['Event', 'Private', 'Lieu', 'Portail', 'Piege'])) or (not hat and key not in ['Attribut']):
                if isinstance(f[key], str):
                    f[key] = sg.re_partition_multiple(f[key], r'{.+?}')
                elif isinstance(f[key], dict):
                    f[key] = Hook.format2ui(f[key], False)
        return f

    @classmethod
    def ui2format(cls, ref, f, hat=True):
        for key in ref:
            if (hat and any(k in key for k in ['Event', 'Private', 'Lieu', 'Portail', 'Piege'])) or not hat:
                if isinstance(f[key], (list, set, tuple)):
                    f[key] = ' '.join(f[key])
                elif isinstance(f[key], dict):
                    f[key] = Hook.ui2format(ref[key], f[key], False)
                else:
                    f[key] = f[key]
        return f

    # Update format
    def update_format(self, **kwargs):
        try:
            format = kwargs
            # Filters check
            if sg.CONF_FORMAT_FILTRE not in format:
                format[sg.CONF_FORMAT_FILTRE] = []
            if not isinstance(format[sg.CONF_FORMAT_FILTRE], list) and all(isinstance(filtre, str) for filtre in format[sg.CONF_FORMAT_FILTRE]):
                delattr(format, sg.CONF_FORMAT_FILTRE)
            # Abreviations check
            if sg.CONF_FORMAT_ABREVIATIONS not in format:
                format[sg.CONF_FORMAT_ABREVIATIONS] = {}
            if not isinstance(format[sg.CONF_FORMAT_ABREVIATIONS], dict):
                delattr(format, sg.CONF_FORMAT_ABREVIATIONS)
            # Formats check
            self.format = Hook.ui2format(sg.format, format)
            # Format
            return sg.db.upsert(self)
        except Exception:
            return None

    # Use the hook to get specific treasures
    def get_treasures_for(self, treasures_id):
        if self.jwt is None: return
        # Build the list of active users
        users_id = self.coterie.members_list_sharing(True, None, True)
        # Find the treasures
        del treasures_id[100:]
        treasures = []
        for _id in treasures_id:
            try:
                treasure = sg.db.session.query(TresorPrivate).join(TresorPrivate.tresor_meta) \
                    .filter(and_(TresorPrivate.viewer_id.in_(users_id), TresorPrivate.tresor_id == _id)) \
                    .order_by(TresorPrivate.last_reconciliation_at.desc().nullslast())\
                    .limit(1).all()
                for t in treasure:
                    treasures.append({
                        'id': t.tresor_id,
                        'type': t.type,
                        'nom': t.nom,
                        'templates': t.templates,
                        'mithril': t.mithril,
                        'effet': t.effet,
                    });
            except NoResultFound:
                pass
        return treasures

    # Use the hook to get specific trolls
    def get_trolls_for(self):
        if self.jwt is None: return
        # Build the list of active users
        users_id = self.coterie.members_list_sharing(None, True, True, True)
        # Find the trolls
        trolls = []
        filters = ['statut', 'action', 'resistance', 'maitrise', 'corpulence', 'agilite', 'armure', 'vue', 'regeneration', 'degats', 'attaque', 'esquive', 'reflexe']
        for _id in users_id:
            try:
                troll = sg.db.session.query(TrollPrivate) \
                    .filter(and_(TrollPrivate.viewer_id.in_(users_id), TrollPrivate.troll_id == _id)) \
                    .order_by(TrollPrivate.last_reconciliation_at.desc().nullslast())\
                    .limit(1).all()
                for t in troll:
                    trolls.append({
                        'id': t.troll_id,
                        'nom': t.troll.nom,
                        'niv': t.troll.niv,
                        'race': t.troll.race,
                        'pdv': t.pdv,
                        'pdv_max': t.pdv_max,
                        'dla': t.next_dla.strftime('%d/%m %H:%M:%S') if t.next_dla else None,
                        'fatigue': t.str_fatigue,
                        'pa': t.pa,
                        'concentration': t.concentration,
                        'pos_x': t.pos_x,
                        'pos_y': t.pos_y,
                        'pos_n': t.pos_n,
                        'pos_n': t.pos_n,
                        'statut': t.statut,
                        'caracs': '\n'.join(sg.no.stringify(t, filters=filters, stringifyTrollCapa=False).split('\n')[1:])
                    });
            except NoResultFound:
                pass
        return trolls

    # Use the hook to get specific mushrooms
    def get_mushrooms_for(self, mushrooms_id):
        if self.jwt is None: return
        # Build the list of active users
        users_id = self.coterie.members_list_sharing(True, None, True)
        # Find the mushrooms
        del mushrooms_id[100:]
        mushrooms = []
        for _id in mushrooms_id:
            try:
                mushroom = sg.db.session.query(ChampiPrivate) \
                    .filter(and_(ChampiPrivate.viewer_id.in_(users_id), ChampiPrivate.champi_id == _id), ChampiPrivate.nom != None) \
                    .order_by(ChampiPrivate.last_event_update_at.desc().nullslast(),
                              ChampiPrivate.last_seen_at.desc().nullslast()) \
                    .limit(1).all()
                for m in mushroom:
                    mushrooms.append({
                        'id': m.champi_id,
                        'nom': m.nom,
                        'qualite': m.qualite,
                    });
            except NoResultFound:
                pass
        return mushrooms

    # Use the hook to get specific traps
    def get_traps_for(self, pos_x, pos_y, pos_n, view_h, view_v):
        if self.jwt is None: return
        # Build the list of active users
        users_id = self.coterie.members_list_sharing(True, None, True)
        # Find the traps
        traps = []
        try:
            _traps = sg.db.session.query(Piege) \
                .filter(and_(Lieu.pos_x >= pos_x - view_h, Lieu.pos_x <= pos_x + view_h,
                             Lieu.pos_y >= pos_y - view_h, Lieu.pos_y <= pos_y + view_h,
                             Lieu.pos_n >= pos_n - view_v, Lieu.pos_n <= pos_n + view_v,
                             Lieu.owner_id.in_(users_id), Lieu.destroyed == False)) \
                .order_by(Lieu.last_seen_at.desc().nullslast()).all()
            for t in _traps:
                traps.append({
                    'id': t.id,
                    'owner_id': t.owner_id,
                    'pos_x': t.pos_x,
                    'pos_y': t.pos_y,
                    'pos_n': t.pos_n,
                    'type': t.piege_type,
                    'mm': t.piege_mm,
                    'creation_datetime': sg.format_time(t.creation_datetime)
                });
        except NoResultFound:
            pass
        return traps

    # Use the hook to get specific events
    def get_events_for(self, being_id, start_time, end_time):
        if self.jwt is None: return
        # Build the list of active users
        users_id = self.coterie.members_list_sharing(None, None, True)
        # Find the events
        try:
            filter = and_(Event.owner_id.in_(users_id),
                      Event.time >= datetime.datetime.fromtimestamp(start_time / 1000.0),
                      Event.time <= datetime.datetime.fromtimestamp(end_time / 1000.0),
                      or_(
                          Event.mail_subject.ilike('%' + str(being_id) + '%'),
                          Event.mail_body.ilike('%' + str(being_id) + '%')
                      ))
            events = sg.db.session.query(Event).filter(filter).order_by(asc(Event.time)).limit(50).all()
        except NoResultFound as e:
            events = []
        # Stringify the events
        res = []
        for event in events:
            r = {'time': sg.format_time(event.time),
                 'message': sg.no.stringify(event, self.format),
                 'owner_id': event.owner_id,
                 'owner_nom': event.owner_nom,
                 'icon': event.icon(),
                 }
            if isinstance(event, battleEvent):
                r['att_id'] = event.att_id
                r['att_nom'] = event.att_nom
                r['def_id'] = event.def_id
                r['def_nom'] = event.def_nom
            elif isinstance(event, cdmEvent):
                r['mob_id'] = event.mob_id
                r['mob_nom'] = event.mob_nom
            elif isinstance(event, tresorEvent):
                r['tresor_id'] = event.tresor_id
                r['tresor_nom'] = event.nom
            elif isinstance(event, champiEvent):
                r['champi_id'] = event.champi_id
                r['champi_nom'] = event.nom
            elif isinstance(event, aaEvent):
                r['troll_id'] = event.troll_id
                r['troll_nom'] = event.troll_nom
            elif isinstance(event, cpEvent):
                r['piege_id'] = event.piege_id
                r['piege_type'] = event.piege_type
            elif isinstance(event, tpEvent):
                r['portail_id'] = event.portail_id
            res.append(r)
        return res

    # Trigger the hook
    def trigger(self, force=False):
        if self.jwt is None and not force: return
        if self.last_event_id is None: self.last_event_id = 0
        # Build the list of active users
        users_id = self.coterie.members_list_sharing(None, None, True, None)
        users_id_withHookPropagation = self.coterie.members_list_sharing(None, None, True, True)
        # Find the events
        try:
            events = sg.db.session.query(Event).filter(Event.owner_id.in_(users_id), Event.id > self.last_event_id, datetime.datetime.now() - Event.time < datetime.timedelta(hours=24)).order_by(asc(Event.time)).all()
        except NoResultFound as e:
            events = []
        # Stringify the events
        max_id, res = 0, []
        for event in events:
            max_id = max(event.id, max_id)
            if event.owner_id in users_id_withHookPropagation:
                res.append({'id': event.id, 'message': sg.no.stringify(event, self.format)})
        # Update the hook
        if max_id > 0 and self.last_event_id is not None and max_id > self.last_event_id:
            self.last_event_id = max_id
            sg.db.upsert(self)
        # If it's a reverse hook, push it
        if self.type in sg.conf[sg.CONF_HOOK_SECTION]:
            url = sg.conf[sg.CONF_HOOK_SECTION][self.type][sg.CONF_HOOK_URL]
            if url is not None and url != '':
                try:
                    requests.post(url, headers={'Authorization': self.jwt}, data={'events': json.dumps(res)})
                except Exception as e:
                    sg.logger.warning('Failed to push \'%s\' hook for group \'%s\' (%s) at url \'%s\' : %s' % (self.type, self.coterie.nom, self.coterie_id, url, e))
        return res
