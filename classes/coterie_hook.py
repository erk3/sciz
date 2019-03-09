#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.event import Event
from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, UniqueConstraint, asc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship
import copy, requests, json
import modules.globals as sg


# CLASS DEFINITION
class Hook(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Coterie identifier
    coterie_id = Column(Integer, ForeignKey('coterie.id'))
    # Type of hook (can currently be Miaou, Hangouts or Discord)
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

    # Trigger the hook
    def trigger(self, force=False):
        if self.jwt is None and not force: return
        if self.last_event_id is None: self.last_event_id = 0
        # Build the list of active users
        users_id = self.coterie.members_list_sharing(None, None, True)
        # Find the events
        try:
            events = sg.db.session.query(Event).filter(Event.owner_id.in_(users_id), Event.id > self.last_event_id).order_by(asc(Event.time)).all()
        except NoResultFound as e:
            events = []
        # Stringify the events
        max_id, res = 0, []
        for event in events:
            max_id = max(event.id, max_id)
            res.append({'id': event.id, 'message': sg.no.stringify(event, self.format)})
        # Update the hook
        if len(res) > 0:
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
