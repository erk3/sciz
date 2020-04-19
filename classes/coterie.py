#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.event import Event
from classes.event_cdm import cdmEvent
from classes.event_aa import aaEvent
from classes.event_tresor import tresorEvent
from classes.event_battle import battleEvent
from classes.user_partage import Partage
from classes.coterie_hook import Hook
from sqlalchemy import event, inspect, Column, Integer, Boolean, String, JSON, desc
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship
import datetime
import modules.globals as sg


# CLASS DEFINITION
class Coterie(sg.sqlalchemybase):

    # Constructor is handled by SqlAlchemy, do not override

    # Unique identifier
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Name
    nom = Column(String(150), nullable=False)
    # Description
    desc = Column(String(250))
    # URI for an avatar
    blason_uri = Column(String(500))
    # Type of Coterie, can be personnal or grouped
    grouped = Column(Boolean, default=True)
    # Webpad
    webpad = Column(JSON)

    # Associations
    partages = relationship('Partage', back_populates='coterie', primaryjoin='Coterie.id == Partage.coterie_id', cascade='all,delete-orphan')
    hooks = relationship('Hook', back_populates='coterie', primaryjoin='Coterie.id == Hook.coterie_id', cascade='all,delete-orphan')
    hook_miaou = relationship('Hook', primaryjoin='and_(Coterie.id == Hook.coterie_id, Hook.type == "Miaou")', uselist=False)
    hook_hangouts = relationship('Hook', primaryjoin='and_(Coterie.id == Hook.coterie_id, Hook.type == "Hangouts")', uselist=False)
    hook_discord = relationship('Hook', primaryjoin='and_(Coterie.id == Hook.coterie_id, Hook.type == "Discord")', uselist=False)
    hook_mountyzilla = relationship('Hook', primaryjoin='and_(Coterie.id == Hook.coterie_id, Hook.type == "Mountyzilla")', uselist=False)

    # SQL Table Mapping
    __tablename__ = 'coterie'

    @hybrid_property
    def mp_link(self):
        users_id = ''
        for partage in self.partages_actifs:
            users_id += str(partage.user_id) if users_id == '' else ',' + str(partage.user_id)
        return sg.conf[sg.CONF_MH_SECTION][sg.CONF_LINK_MP] + users_id

    @hybrid_property
    def px_link(self):
        users_id = ''
        for partage in self.partages_actifs:
            users_id += str(partage.user_id) if users_id == '' else ',' + str(partage.user_id)
        return sg.conf[sg.CONF_MH_SECTION][sg.CONF_LINK_PX] + users_id

    def members_list_sharing(self, view=None, profil=None, events=None, checkProp=None):
        users_id = []
        for partage in self.partages_actifs:
            if partage.user_id not in users_id:
                if (view is None or view == partage.sharingView)\
                        and (profil is None or profil == partage.sharingProfile)\
                        and (events is None or (partage.sharingEvents and (checkProp is None or partage.hookPropagation))):
                    users_id.append(partage.user_id)
        return users_id

    @hybrid_property
    def partages_actifs(self):
        if self.partages is not None:
            now = datetime.datetime.now()
            return list(filter(lambda x: not x.pending and ((x.start is None or x.start < now) and (x.end is None or now < x.end)), self.partages))
        return None

    @hybrid_property
    def partages_inactifs(self):
        if self.partages is not None:
            now = datetime.datetime.now()
            return list(filter(lambda x: x.pending or ((x.start is not None and x.start >= now) or (x.end is not None and now >= x.end)), self.partages))
        return None

    @hybrid_property
    def partages_admins(self):
        if self.partages is not None:
            return list(filter(lambda x: x.admin, self.partages_actifs))
        return None

    @hybrid_property
    def partages_utilisateurs(self):
        if self.partages is not None:
            return list(filter(lambda x: not x.admin, self.partages_actifs))
        return None

    @hybrid_property
    def partages_expires(self):
        if self.partages is not None:
            now = datetime.datetime.now()
            return list(filter(lambda x: (x.start is not None and x.start >= now) or (x.end is not None and now >= x.end), self.partages))
        return None

    @hybrid_property
    def partages_invitations(self):
        if self.partages is not None:
            now = datetime.datetime.now()
            return list(filter(lambda x: x.pending and ((x.start is None or x.start < now) and (x.end is None or now < x.end)), self.partages))
        return None

    def has_partage(self, user_id, admin=False):
        return any(p.user_id == user_id and (not admin or p.admin) for p in self.partages_actifs)

    def has_pending_partage(self, user_id):
        return any(p.user_id == user_id for p in self.partages_invitations)

    def update(self, updater_id, **kwargs):
        is_admin = self.has_partage(updater_id, True)
        if is_admin:
            for attr in ['nom', 'desc', 'blason_uri']:
                if attr in kwargs and kwargs.get(attr) is not None:
                    setattr(self, attr, kwargs.get(attr))
        for attr in ['webpad']:
            if attr in kwargs and kwargs.get(attr) is not None:
                setattr(self, attr, kwargs.get(attr))
        if 'partages' in kwargs and self.grouped:
            now = datetime.datetime.now()
            partages = kwargs.get('partages')
            # Add invites
            if is_admin:
                for id in partages['pendingToAdd']:
                    if not self.has_pending_partage(id):
                        partage = Partage(coterie_id=self.id, user_id=id, pending=True)
                        self.partages.append(partage)
            # Expire shares
            if is_admin:
                for id in partages['toExpire']:
                    if self.has_pending_partage(id) or self.has_partage(id):
                        partage = sg.db.session.query(Partage).filter(Partage.coterie_id==self.id, Partage.user_id==id).order_by(desc(Partage.id)).first()
                        partage.end = now
            # Update admins and users
            for user in partages['admins'] + partages['users']:
                partage = sg.db.session.query(Partage).filter(Partage.coterie_id==self.id, Partage.user_id==user['partage']['user_id']).order_by(desc(Partage.id)).first()
                if is_admin:
                    if not (partage.admin and len(self.partages_admins) <= 1):
                        partage.admin = user['partage']['admin']
                    partage.hookPropagation = user['partage']['hookPropagation']
                if partage.user_id == updater_id:
                    partage.sharingEvents = user['partage']['sharingEvents']
                    partage.sharingProfile = user['partage']['sharingProfile']
                    partage.sharingView = user['partage']['sharingView']
                    partage.hookPropagation = user['partage']['hookPropagation']

        return sg.db.upsert(self)

    @classmethod
    def create(cls, user_id, nom, blason_uri, desc, grouped=True):
        coterie = Coterie(nom=nom, blason_uri=blason_uri, desc=desc, grouped=grouped)
        coterie = sg.db.upsert(coterie)
        # Create the hooks for this group
        for type in sg.conf[sg.CONF_HOOK_SECTION]:
            hook = Hook(coterie_id=coterie.id, type=type)
            hook = sg.db.upsert(hook)
        # Share of the user creating the group
        partage = Partage(coterie_id=coterie.id, user_id=user_id, admin=True, start=datetime.datetime.now())
        return sg.db.upsert(partage)

    # Get the events
    def get_events(self, limit, offset, last_time, revert=False):
        # Build the list of active users
        users_id = self.members_list_sharing(None, None, True)
        # Find the events
        try:
            if not revert:
                events = sg.db.session.query(Event).filter(Event.owner_id.in_(users_id), Event.time > datetime.datetime.fromtimestamp(last_time / 1000.0)).order_by(desc(Event.time), desc(Event.id)).offset(offset).limit(limit).all()
            else:
                events = sg.db.session.query(Event).filter(Event.owner_id.in_(users_id), Event.time <= datetime.datetime.fromtimestamp(last_time / 1000.0)).order_by(desc(Event.time), desc(Event.id)).offset(offset).limit(limit).all()
        except NoResultFound as e:
            events = []
        # Stringify the events
        res = []
        for event in events:
            e = sg.row2dictfull(event)
            if isinstance(event, cdmEvent):
                e['mob_blason_uri'] = event.mob.blason_uri
                e['mob_link'] = event.mob.link
            if isinstance(event, aaEvent):
                e['troll_blason_uri'] = event.troll.blason_uri
                e['troll_link'] = event.troll.link
            if isinstance(event, tresorEvent):
                e['tresor_nom'] = event.str_nom_complet
                e['tresor_link'] = event.tresor.link
            if isinstance(event, battleEvent):
                e['att_blason_uri'] = event.att_being.blason_uri if event.att_being is not None else None
                e['def_blason_uri'] = event.def_being.blason_uri if event.def_being is not None else None
                e['autre_blason_uri'] = event.autre_being.blason_uri if event.autre_being is not None else None
                e['att_link'] = event.att_being.link if event.att_being is not None else None
                e['def_link'] = event.def_being.link if event.def_being is not None else None
                e['autre_link'] = event.autre_being.link if event.autre_being is not None else None
                e['subtype'] = event.subtype
                e['arm'] = event.arm
            e['owner_blason_uri'] = event.owner.blason_uri
            e['owner_link'] = event.owner.link
            obj = {'event': e, 'repr': sg.no.stringify(event), 'icon': event.icon()}
            res.append(obj)
        return res
