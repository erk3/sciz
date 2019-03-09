#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.being_troll import Troll
from classes.user_mh_call import MhCall
from classes.coterie import Coterie
from sqlalchemy import desc, event, Column, Integer, String, inspect, ForeignKey, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, object_session
import random, string, hashlib, base64, os, bcrypt, datetime
import modules.globals as sg


# CLASS DEFINITION
class User(sg.sqlalchemybase):

    # Constructor is handled by SQLAlchemy, do not override

    # Unique identifier of the player
    id = Column(Integer, ForeignKey('being_troll.id'), primary_key=True)
    # Pseudonyme
    pseudo = Column(String(50), nullable=False)
    # Password
    pwd_hash = Column(String(550), nullable=False)
    # SCIZ mail
    mail = Column(String(255), nullable=False)
    # SCIZ mail hash pwd
    mail_pwd_hash = Column(String(500), nullable=False)
    # User mail
    user_mail = Column(String(255))
    # Mountyhall API Key
    mh_api_key = Column(String(50))
    # Maximum number of calls to dynamic section MH SP defined by the user
    max_mh_sp_dynamic = Column(Integer(), default=12)
    # Maximum number of calls to static section MH SP defined by the user
    max_mh_sp_static = Column(Integer(), default=5)
    # Web session duration
    web_session_duration = Column(Integer(), default=60)
    # Community sharing
    community_sharing = Column(Boolean, default=True)

    # Associations
    troll = relationship('Troll', back_populates='user', primaryjoin='User.id == Troll.id')
    mh_calls = relationship('MhCall', back_populates='user', primaryjoin='User.id == MhCall.user_id', lazy='dynamic', cascade='all,delete-orphan')
    partages = relationship('Partage', back_populates='user', primaryjoin='User.id == Partage.user_id', cascade='all,delete-orphan')

    # SQL Table Mapping
    __tablename__ = 'user'

    @hybrid_property
    def blason_uri(self):
        if self.troll is not None and self.troll.blason_uri is not None:
            return self.troll.blason_uri
        return None

    @hybrid_property
    def nom(self):
        if self.pseudo is None or self.pseudo == '':
            if self.troll is not None and self.troll.nom is not None:
                return self.troll.nom
            return None
        return self.pseudo

    @hybrid_property
    def should_refresh_dynamic_sp(self):
        now = datetime.datetime.now()
        since = now - datetime.timedelta(hours=24)
        count = self.mh_calls.filter(MhCall.time > since, MhCall.status == 0, MhCall.type == 'Dynamique').count()
        last = self.mh_calls.filter(MhCall.type == 'Dynamique').order_by(desc(MhCall.time)).first()
        max_mh_sp_dynamic = max(0, min(24, self.max_mh_sp_dynamic if last.status == 0 else 24))
        return count <= max_mh_sp_dynamic and (last is None or (now - last.time).total_seconds() > 24 * 3600 / max_mh_sp_dynamic)

    @hybrid_property
    def should_refresh_static_sp(self):
        now = datetime.datetime.now()
        since = now - datetime.timedelta(hours=24)
        count = self.mh_calls.filter(MhCall.time > since, MhCall.status == 0, MhCall.type == 'Statique').count()
        last = self.mh_calls.filter(MhCall.type == 'Statique').order_by(desc(MhCall.time)).first()
        max_mh_sp_static = max(0, min(10, self.max_mh_sp_static if last.status == 0 else 10))
        return count <= max_mh_sp_static and (last is None or (now - last.time).total_seconds() > 24 * 3600 / max_mh_sp_static)

    @hybrid_property
    def partages_groupe(self):
        if self.partages is not None:
            return list(filter(lambda x: x.coterie.grouped, self.partages))
        return None

    @hybrid_property
    def partages_actifs(self):
        if self.partages is not None:
            now = datetime.datetime.now()
            return list(filter(lambda x: not x.pending and ((x.start is None or x.start < now) and (x.end is None or now < x.end)), self.partages_groupe))
        return None

    @hybrid_property
    def partages_inactifs(self):
        if self.partages is not None:
            now = datetime.datetime.now()
            return list(filter(lambda x: x.pending or ((x.start is not None and x.start >= now) or (x.end is not None and now >= x.end)), self.partages_groupe))
        return None

    @hybrid_property
    def partages_admins(self):
        if self.partages is not None:
            return list(filter(lambda x: x.admin, self.partages_actifs))
        return None

    @hybrid_property
    def partage_perso(self):
        if self.partages is not None:
            return list(filter(lambda x: not x.coterie.grouped, self.partages))[0]
        return None

    @hybrid_property
    def partages_invitations(self):
        if self.partages is not None:
            now = datetime.datetime.now()
            return list(filter(lambda x: x.pending and ((x.start is None or x.start < now) and (x.end is None or now < x.end)), self.partages))
        return None

    @classmethod
    def authenticate(cls, **kwargs):
        id = kwargs.get('id')
        pwd = kwargs.get('pwd')
        if id is None or not id.isdigit() or pwd is None:
            return None, 'Données de formulaire invalides'
        user = sg.db.session.query(User).filter(User.id == int(id)).first()
        if user is None or not bcrypt.checkpw(pwd.encode(sg.DEFAULT_CHARSET), user.pwd_hash.encode(sg.DEFAULT_CHARSET)):
            return None, 'Identifiants invalides'
        return user, ''

    @classmethod
    def register(cls, **kwargs):
        id = kwargs.get('id')
        pwd = kwargs.get('pwd')
        pwd2 = kwargs.get('pwd2')
        pwd_mh = kwargs.get('pwd_mh')
        if any(a is None for a in [id, pwd, pwd2, pwd_mh]) or not id.isdigit() or pwd != pwd2 or len(pwd) < 8:
            return None, 'Données de formulaire invalides'
        user = sg.db.session.query(User).get(id)
        if user is not None:
            return None, 'Cet utilisateur existe déjà...'
        user = User(id=id, pseudo='', pwd_hash=pwd, mh_api_key=pwd_mh)
        user = sg.db.upsert(user)
        mh_call = True
        try:
            mh_call = sg.mc.profil4_sp_call(user)
        except Exception as e:
            mh_call = False
        if not mh_call:
            sg.db.delete(user)
            return None, 'Impossible de vérifier le mot de passe d\'application MH'
        else:
            troll = sg.db.session.query(Troll).get(id)
            if troll is not None:
                user.pseudo = troll.nom
                user = sg.db.upsert(user)
        return user, ''

    def members_list_sharing(self, view=None, profil=None, events=None):
        users_id = []
        for my_partage in self.partages_actifs:
            for partage in my_partage.coterie.partages_actifs:
                if partage.user_id not in users_id:
                    if (view is None or view == partage.sharingView)\
                            and (profil is None or profil == partage.sharingProfile)\
                            and (events is None or partage.sharingEvents):
                        users_id.append(partage.user_id)
        return users_id

    def update(self, **kwargs):
        try:
            self.pseudo = kwargs.get('pseudo')[:50]
            self.user_mail = kwargs.get('user_mail')
            self.web_session_duration = int(kwargs.get('session')) * 60
            if not (1 * 60 <= self.web_session_duration <= 24 * 60):
                return None
            self.mh_api_key = kwargs.get('pwd_mh')
            self.max_mh_sp_dynamic = int(kwargs.get('max_sp_dyn'))
            self.community_sharing = kwargs.get('community_sharing')
            if not (0 <= self.max_mh_sp_dynamic <= 24 and 0 <= self.max_mh_sp_static <= 10):
                return None
            return sg.db.upsert(self)
        except Exception as e:
            return None

    def resetPassword(self, **kwargs):
        pwd = kwargs.get('pwd')
        new_pwd = kwargs.get('new_pwd')
        new_pwd2 = kwargs.get('new_pwd2')
        if any(a is None for a in [pwd, new_pwd, new_pwd2]) or new_pwd != new_pwd2 or len(new_pwd) < 8 or not bcrypt.checkpw(pwd.encode(sg.DEFAULT_CHARSET), self.pwd_hash.encode(sg.DEFAULT_CHARSET)):
            return None, 'Données invalides...'
        self.pwd_hash = new_pwd
        return sg.db.upsert(self), ''


# SQLALCHEMY LISTENERS (same listener types executed in order)
@event.listens_for(User, 'before_insert')
def generate_random_mail(mapper, connection, target):
    domain_name = sg.conf[sg.CONF_MAIL_SECTION][sg.CONF_MAIL_DOMAIN_NAME]
    r = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(8))
    target.mail = '{}.{}@{}'.format(target.id, r, domain_name)


@event.listens_for(User, 'before_insert')
def generate_random_mail_pwd_hash(mapper, connection, target):
    # Generate a random long whatever
    # (mail_pwd is used for maintaining postfix-accounts.cf but accounts should not be used by end-users)
    pwd = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(42))
    salt = os.urandom(64) # Creates a random 64 byte string
    sha_hash = hashlib.sha512()
    sha_hash.update(pwd.encode(sg.DEFAULT_CHARSET))
    sha_hash.update(salt)
    sha_hash_salt = sha_hash.digest() + salt
    pwd_hash = base64.b64encode(sha_hash_salt)
    target.mail_pwd_hash = '{{SSHA512}}{}'.format(pwd_hash.decode(sg.DEFAULT_CHARSET))


@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def hash_password(mapper, connection, target):
    state = inspect(target)
    hist = state.get_history('pwd_hash', True)
    if hist.has_changes() and target.pwd_hash is not None and isinstance(target.pwd_hash, str):
        target.pwd_hash = bcrypt.hashpw(target.pwd_hash.encode(sg.DEFAULT_CHARSET), bcrypt.gensalt(12)).decode(sg.DEFAULT_CHARSET)


@event.listens_for(User, 'before_insert')
def create_public_troll(mapper, connection, target):
    if sg.db.session.query(Troll).get(target.id) is None:
        sg.db.upsert(Troll(id=target.id, nom=target.pseudo))


@event.listens_for(User, 'before_insert')
def create_own_coterie(mapper, connection, target):
    @event.listens_for(object_session(target), 'after_commit')
    def create_partage_after_commit(session):
        if sg.db.session.query(User).get(target.id) is not None:
            Coterie.create(target.id, 'Ma coterie privée', '', '', False)
