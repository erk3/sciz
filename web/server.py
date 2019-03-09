#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.user import User
from classes.user_mh_call import MhCall
from classes.user_partage import Partage
from classes.coterie import Coterie
from classes.coterie_hook import Hook
from classes.being import Being
from classes.being_troll import Troll
from classes.being_troll_private import TrollPrivate
from classes.being_mob import Mob
from classes.being_mob_private import MobPrivate
from classes.tresor import Tresor
from classes.tresor_private import TresorPrivate
from classes.champi import Champi
from classes.champi_private import ChampiPrivate
from classes.lieu import Lieu
from classes.event import Event
from classes.event_cdm import cdmEvent
from modules.mh_caller import MhCaller
from functools import wraps
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_claims, get_jwt_identity
from flask_jwt_extended.view_decorators import _decode_jwt_from_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from sqlalchemy import func, or_, and_, asc, desc
import datetime, dateutil.relativedelta, json, math, re, sys, logging
import modules.globals as sg


# WEBAPP DEFINITION
webapp = Flask('SCIZ', static_folder='./web/dist-public/static', template_folder='./web/dist-public/template')
if webapp.debug or webapp.testing or webapp.env != 'production':
    cors = CORS(webapp, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager()

# WEBAPP CONFIG
@webapp.before_first_request
def configure():
    # SCIZ startup
    if sg.sciz is None:
        try:
            from sciz import SCIZ
            sciz = SCIZ('confs/sciz_main.yaml', 'INFO')
            sg.logger.info('The bats woke up!')
            sg.logger.info('Starting the web server...')
            sg.logger = logging.getLogger('server')
        except Exception as e:
            print('The bats went sick. Check the log file?', file=sys.stderr)
            if sg.logger is not None:
                sg.logger.exception(e)
            else:
                traceback.print_exc()
            sys.exit(1)
    webapp.config['JWT_SECRET_KEY'] = sg.conf[sg.CONF_WEB_SECTION][sg.CONF_WEB_SECRET]
    webapp.config['JWT_TOKEN_LOCATION'] = 'headers'
    webapp.config['JWT_HEADER_NAME'] = 'Authorization'
    webapp.config['JWT_HEADER_TYPE'] = ''
    jwt.init_app(webapp)

@webapp.errorhandler(500)
def internal_error(error):
    sg.db.session.rollback()
    return render_template('index.html')

# JWT CONFIG
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    now = datetime.datetime.now()
    if isinstance(identity, User):
        return {
            'hook_type': 'USER',
            'id': identity.id,
            'iat': now,
            'exp': now + datetime.timedelta(minutes=identity.web_session_duration),
            'dom': sg.conf[sg.CONF_WEB_SECTION][sg.CONF_WEB_DOMAIN],
            'sec': sg.conf[sg.CONF_WEB_SECTION][sg.CONF_WEB_TLS]
        }
    elif isinstance(identity, Hook):
        return {'hook_type': 'HOOK', 'id': identity.id, 'type': identity.type}
    else:
        return { 'id': identity.id }

def user_jwt_check(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        jwt_data = _decode_jwt_from_request(request_type='access')
        authorized = jwt_data['user_claims']['hook_type'] == 'USER'
        if not authorized: raise NoAuthorizationError('Non autorisé')
        return view_function(*args, **kwargs)
    return jwt_required(wrapper)

def hook_jwt_check(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        jwt_data = _decode_jwt_from_request(request_type='access')
        authorized = jwt_data['user_claims']['hook_type'] == 'HOOK'
        if not authorized:
            raise NoAuthorizationError('Non autorisé')
        if sg.db.session.query(Hook).filter(Hook.jwt==request.headers['Authorization']).count() < 1:
            raise NoAuthorizationError('Hook révoqué')
        return view_function(*args, **kwargs)
    return jwt_required(wrapper)

# ROUTES DEFINITION

# STATS
@webapp.route('/api/stats', methods=('GET',))
def stats():
    now = datetime.datetime.now()
    user_count = sg.db.session.query(User).count()
    event_count_last_month = sg.db.session.query(Event).filter(Event.time > now + dateutil.relativedelta.relativedelta(months=-1)).count()
    res = jsonify(user_count=user_count, event_count_last_month=event_count_last_month)
    return res, 200

# LOGIN & REGISTER
@webapp.route('/api/login', methods=('POST',))
@webapp.route('/api/register', methods=('POST',))
def login_register():
    data = request.get_json()
    user, error = User.register(**data) if 'register' in request.url_rule.rule else User.authenticate(**data)
    if user is None:
        return jsonify(message=error), 400
    user = sg.db.session.query(User).get(user.id)
    user_flat = {'id': user.id, 'nom': user.nom, 'blason_uri': user.blason_uri}
    res = jsonify(jwt=create_access_token(identity=user, expires_delta=datetime.timedelta(minutes=user.web_session_duration)), user=user_flat)
    return res, 200

# MOBS
@webapp.route('/api/mobs', methods=('GET',))
@user_jwt_check
def get_mobs_list():
    cdms = sg.db.session.query(cdmEvent).outerjoin(User, cdmEvent.owner_id == User.id).filter(User.community_sharing == True).distinct(cdmEvent.mob_nom, cdmEvent.mob_age).group_by(Event.id, cdmEvent.id, cdmEvent.mob_nom, cdmEvent.mob_age).all()
    l = []
    for cdm in cdms:
        l.append({'nom': cdm.mob_nom + ' [' + cdm.mob_age + ']', 'blason_uri': cdm.mob.blason_uri})
    res = jsonify(l)
    return res, 200

@webapp.route('/api/nbCDM', methods=('GET',))
@user_jwt_check
def get_nb_cdm():
    res = jsonify(sg.db.session.query(cdmEvent).outerjoin(User, cdmEvent.owner_id == User.id).filter(User.community_sharing == True).count())
    return res, 200

# USER PROFIL
@webapp.route('/api/users/<int:id>', methods=('GET',))
@user_jwt_check
def get_users_list(id):
    coterie = sg.db.session.query(Coterie).get(id)
    users = sg.db.session.query(User).all()
    l = []
    for u in users:
        if u.id != get_jwt_identity() and not coterie.has_partage(u.id, False):
            l.append({'id': u.id, 'nom': u.nom, 'blason_uri': u.blason_uri})
    res = jsonify(l)
    return res, 200

@webapp.route('/api/profil', methods=('GET',))
@user_jwt_check
def get_profil():
    user = sg.db.session.query(User).get(get_jwt_identity())
    res = jsonify(pseudo=user.nom, sciz_mail=user.mail, user_mail=user.user_mail,
                  session=user.web_session_duration // 60, pwd_mh=user.mh_api_key,
                  max_sp_dyn=user.max_mh_sp_dynamic, max_sp_sta=user.max_mh_sp_static,
                  community_sharing=user.community_sharing)
    return res, 200

@webapp.route('/api/profil', methods=('POST',))
@user_jwt_check
def set_profil():
    data = request.get_json()
    user = sg.db.session.query(User).get(get_jwt_identity())
    user = user.update(**data)
    if user is None:
        return jsonify(message='Une erreur est survenue...'), 400
    return jsonify(message='Profil sauvegardé !'), 200

@webapp.route('/api/profil', methods=('DELETE',))
@user_jwt_check
def delete_profil():
    user = sg.db.session.query(User).get(get_jwt_identity())
    # If the only admin of a group delete its account then everybody becomes admin
    # If there is nobody with an active share, then the group is deleted
    for partage in user.partages:
        if len(partage.coterie.partages_actifs) < 1:
            sg.db.delete(partage.coterie)
        if partage.coterie.has_partage(user.id, True) and len(partage.coterie.partages_admins) <= 1:
            for partage_user in partage.coterie.partages_utilisateurs:
                partage_user.admin = True
                sg.db.upsert(partage_user)
    sg.db.delete(user)
    return jsonify(message='Profil supprimé !'), 200

@webapp.route('/api/calls/<int:page>', methods=('GET',))
@user_jwt_check
def get_mh_calls(page):
    total_calls = sg.db.session.query(MhCall).filter(MhCall.user_id == get_jwt_identity()).count()
    calls = sg.db.session.query(MhCall).filter(MhCall.user_id == get_jwt_identity()).order_by(MhCall.time.desc()).offset(min(total_calls, 10 * (page - 1))).limit(10).all()
    return jsonify(total=total_calls, calls=[sg.row2dict(c) for c in calls]), 200

@webapp.route('/api/resetPassword', methods=('POST',))
@user_jwt_check
def reset_password():
    data = request.get_json()
    user = sg.db.session.query(User).get(get_jwt_identity())
    user, error = user.resetPassword(**data)
    if user is None:
        return jsonify(message=error), 400
    return jsonify(message='Mot de passe modifié !'), 200

# GROUPS
@webapp.route('/api/groups/<path:path>', methods=('GET',))
@webapp.route('/api/groups', defaults={'path': ''}, methods=('GET',))
@user_jwt_check
def get_coteries(path):
    user = sg.db.session.query(User).get(get_jwt_identity())
    # Shares
    partage_perso = user.partage_perso
    partages_actifs = user.partages_actifs
    partages_invitations = user.partages_invitations if 'withinvites' in path else []
    # Groups
    coterie_perso = sg.row2dict(partage_perso.coterie)
    coteries = [sg.row2dict(p.coterie) for p in partages_actifs]
    invitations = [sg.row2dict(p.coterie) for p in partages_invitations]
    # Delete webpad if not necessary
    if not 'withwebpad' in path:
        for c in [coterie_perso] + coteries + invitations:
            c['webpad'] = None
    # Add MP/PX link and hooks if admin ans asked for
    for p, c in zip([partage_perso] + partages_actifs + partages_invitations, [coterie_perso] + coteries + invitations):
        c['mp_link'] = p.coterie.mp_link
        c['px_link'] = p.coterie.px_link
        if 'withhooks' in path and p.admin:
            c['hooks'] = [sg.row2dict(h) for h in p.coterie.hooks]
    # Result
    return jsonify(coterie_perso=coterie_perso, coteries=coteries, invitations=invitations), 200

@webapp.route('/api/group/<int:id>/webpad', methods=('GET',))
@webapp.route('/api/group/<int:id>', methods=('GET',))
@user_jwt_check
def get_coterie(id):
    coterie = sg.db.session.query(Coterie).get(id)
    if not 'webpad' in request.url_rule.rule:
        delattr(coterie, 'webpad')
    c = sg.row2dict(coterie)
    c['px_link'] = coterie.px_link
    c['mp_link'] = coterie.mp_link
    if coterie.has_partage(get_jwt_identity(), False):
        return jsonify(coterie=c), 200
    elif coterie.has_partage(get_jwt_identity(), True):
        return jsonify(coterie=c, hooks=sg.row2dict(coterie.hooks)), 200
    return jsonify(message='Autorisation requise'), 401

@webapp.route('/api/group/<int:id>', methods=('POST',))
@user_jwt_check
def set_coterie(id):
    data = request.get_json()
    coterie = sg.db.session.query(Coterie).get(id)
    coterie.update(get_jwt_identity(), **data) # Admin check is done in routine
    return jsonify(message='Coterie mise à jour'), 200

@webapp.route('/api/group/<int:id>', methods=('DELETE',))
@user_jwt_check
def delete_coterie(id):
    coterie = sg.db.session.query(Coterie).get(id)
    if coterie.has_partage(get_jwt_identity(), True):
        sg.db.delete(coterie)
        return jsonify(message='Coterie supprimée !'), 200
    return jsonify(message='Autorisation requise'), 401

@webapp.route('/api/share/invite/<int:id>', methods=('DELETE', 'POST'))
@user_jwt_check
def accept_or_refuse_invite(id):
    data = request.get_json()
    coterie = sg.db.session.query(Coterie).get(id)
    if coterie.has_pending_partage(get_jwt_identity()):
        now = datetime.datetime.now()
        partage = sg.db.session.query(Partage).filter(Partage.coterie_id==id, Partage.user_id==get_jwt_identity()).order_by(desc(Partage.id)).first()
        if request.method == 'POST':
            partage.pending = False
            partage.start = now
            partage.sharingEvents = data['sharingEvents']
            partage.sharingProfile = data['sharingProfile']
            partage.sharingView = data['sharingView']
            message = 'Invitation acceptée'
        else:
            partage.end = now
            message = 'Invitation déclinée'
        sg.db.upsert(partage)
        return jsonify(message=message), 200
    return jsonify(message='Autorisation requise'), 401

@webapp.route('/api/group/create', methods=('POST',))
@user_jwt_check
def create_coterie():
    data = request.get_json()
    Coterie.create(get_jwt_identity(), data['nom'], data['blason_uri'], data['desc'])
    return jsonify(message='Coterie créée'), 200

@webapp.route('/api/shares/<int:id>', methods=('GET',))
@user_jwt_check
def get_partages(id):
    coterie = sg.db.session.query(Coterie).get(id)
    if coterie.has_partage(get_jwt_identity()) or coterie.has_pending_partage(get_jwt_identity()):
        return jsonify(admins=[{'partage': sg.row2dict(p), 'nom': p.user.pseudo, 'blason_uri': p.user.blason_uri} for p in coterie.partages_admins],
                       users=[{'partage': sg.row2dict(p), 'nom': p.user.pseudo, 'blason_uri': p.user.blason_uri} for p in coterie.partages_utilisateurs],
                       pending=[{'partage': sg.row2dict(p), 'nom': p.user.pseudo, 'blason_uri': p.user.blason_uri} for p in coterie.partages_invitations]), 200
    return jsonify(message='Autorisation requise'), 401

@webapp.route('/api/shares/<int:id>', methods=('DELETE',))
@user_jwt_check
def delete_partage(id):
    coterie = sg.db.session.query(Coterie).get(id)
    if coterie.has_partage(get_jwt_identity(), False) and not (coterie.has_partage(get_jwt_identity(), True) and len(coterie.partages_admins) <= 1):
        now = datetime.datetime.now()
        partage = sg.db.session.query(Partage).filter(Partage.coterie_id==id, Partage.user_id==get_jwt_identity()).order_by(desc(Partage.id)).first()
        partage.end = now
        sg.db.upsert(partage)
        return jsonify(message='Partage supprimé'), 200
    return jsonify(message='Partage non supprimé'), 400

# MAPS
def map_query_builder(type, viewer_id, days, pos_x, pos_y, pos_n, portee, count):
    # Time
    then = datetime.datetime.now() + dateutil.relativedelta.relativedelta(days=-int(days))
    # Get the type we request
    cls_mapper = {'user': TrollPrivate, 'trolls': TrollPrivate,
                  'followers': MobPrivate, 'monsters': MobPrivate,
                  'treasures': TresorPrivate, 'mushrooms': ChampiPrivate,
                  'places': Lieu}
    cls = None if not type in cls_mapper else cls_mapper[type]
    if cls is None:
        return None
    # Special USER case
    if type == 'user':
        user = sg.db.session.query(User).get(viewer_id)
        if count:
            users_id = []
            for partage in user.partages_actifs + [user.partage_perso]:
                for partage in partage.coterie.partages_actifs:
                    if not partage.user_id in users_id:
                        users_id.append(partage.user_id)
            return sg.db.session.query(cls).filter(cls.viewer_id == viewer_id, cls.troll_id.in_(users_id))
        return sg.db.session.query(cls).filter(cls.viewer_id == viewer_id, cls.troll_id == viewer_id)
    # Check for parameters and compute some thing
    if pos_x is None or pos_y is None or portee is None:
        return None
    try:
        pos_x, pos_y, portee = int(pos_x), int(pos_y), int(portee)
        pos_n = int(pos_n) if pos_n is not None else None
    except (TypeError, ValueError) as e:
        return None
    pos_x_min = pos_x - portee
    pos_x_max = pos_x + portee
    pos_y_min = pos_y - portee
    pos_y_max = pos_y + portee
    pos_n_min = math.floor(pos_n - round(portee / 2)) if pos_n is not None else None
    pos_n_max = math.ceil(pos_n + round(portee / 2)) if pos_n is not None else None
    default_filter = and_(cls.pos_x >= pos_x_min, cls.pos_x <= pos_x_max,
                          cls.pos_y >= pos_y_min, cls.pos_y <= pos_y_max,
                          cls.last_seen_at > then)
    default_filter = and_(default_filter, cls.pos_n >= pos_n_min, cls.pos_n <= pos_n_max) if pos_n is not None else default_filter
    default_filter = and_(default_filter, cls.viewer_id == viewer_id) if type != 'places' else default_filter
    # Filters
    filter = default_filter
    if type == 'trolls':
        filter = and_(filter, cls.troll_id != viewer_id)
    if type =='followers':
        filter = and_(filter, Mob.mort == False,
                      or_(Mob.nom.contains('Apprivoisé') == True, Mob.nom.contains('Familier') == True,
                          Mob.nom.contains('Nâ-Hàniym-Hééé') == True, Mob.nom.contains('Golem de Cuir') == True,
                          Mob.nom.contains('Golem de Métal') == True, Mob.nom.contains('Golem de Mithril') == True,
                          Mob.nom.contains('Golem de Papier') == True))
    if type == 'monsters':
        filter = and_(filter, Mob.mort == False,
                      and_(Mob.nom.contains('Apprivoisé') == False, Mob.nom.contains('Familier') == False,
                           Mob.nom.contains('Nâ-Hàniym-Hééé') == False, Mob.nom.contains('Golem de Cuir') == False,
                           Mob.nom.contains('Golem de Métal') == False, Mob.nom.contains('Golem de Mithril') == False,
                           Mob.nom.contains('Golem de Papier') == False))
    # Query
    if count:
        query = sg.db.session.query(func.count(cls.pos_x), cls.pos_x, cls.pos_y)
    else:
        query = sg.db.session.query(cls)
    if type == 'followers' or type == 'monsters':
        query = query.join(Mob, cls.mob_id == Mob.id)
    query = query.filter(filter)
    if count:
        return query.group_by(cls.pos_x, cls.pos_y)
    else:
        return query.order_by(cls.pos_n.desc(), cls.last_seen_at.desc())

@webapp.route('/api/map/user', methods=('GET',))
@user_jwt_check
def get_map_user():
    query = map_query_builder('user', get_jwt_identity(), 0, None, None, None, None, True)
    if query is None:
        return jsonify(message='Jeu de paramètre inconnu !'), 400
    res = query.all()
    res = list(map(lambda x: {'id': x.troll_id, 'nom': x.troll.nom, 'blason_uri': x.troll.blason_uri, 'pos_x': x.pos_x, 'pos_y': x.pos_y, 'pos_n': x.pos_n, 'portee': x.portee, 'last_seen_at': sg.format_time(x.last_seen_at, 'Le %d/%m à %H:%M'), 'tooltip': x.tooltip}, res))
    return jsonify(res), 200

@webapp.route('/api/map/count/<string:type>/<string:days>/<string:portee>/<string:pos_x>/<string:pos_y>', defaults={'pos_n': None}, methods=('GET',))
@webapp.route('/api/map/count/<string:type>/<string:days>/<string:portee>/<string:pos_x>/<string:pos_y>/<string:pos_n>', methods=('GET',))
@user_jwt_check
def get_map_count(type, days, pos_x, pos_y, pos_n, portee):
    query = map_query_builder(type, get_jwt_identity(), days, pos_x, pos_y, pos_n, portee, True)
    if query is None:
        return jsonify(message='Jeu de paramètre inconnu !'), 400
    res = query.all()
    res = list(map(lambda x: {'count': x[0], 'pos_x': x[1], 'pos_y': x[2]}, res))
    return jsonify(res), 200

@webapp.route('/api/map/data/<string:type>/<string:days>/<string:portee>/<string:pos_x>/<string:pos_y>', defaults={'pos_n': None}, methods=('GET',))
@webapp.route('/api/map/data/<string:type>/<string:days>/<string:portee>/<string:pos_x>/<string:pos_y>/<string:pos_n>', methods=('GET',))
@user_jwt_check
def get_map_data(type, days, pos_x, pos_y, pos_n, portee):
    query = map_query_builder(type, get_jwt_identity(), days, pos_x, pos_y, pos_n, portee, False)
    if query is None:
        return jsonify(message='Jeu de paramètre inconnu !'), 400
    res = query.all()
    res = list(map(lambda x: {'pos_n': x.pos_n, 'last_seen_at': sg.format_time(x.last_seen_at, 'Le %d/%m à %H:%M'), 'tooltip': x.tooltip}, res))
    return jsonify(res), 200

# EVENTS
@webapp.route('/api/events/<int:coterie_id>/<int:limit>/<int:offset>/<int:last_time>', methods=('GET',))
@webapp.route('/api/events/<int:coterie_id>/<int:limit>/<int:offset>/<int:last_time>/revert', methods=('GET',))
@user_jwt_check
def get_user_events(coterie_id, limit, offset, last_time):
    coterie = sg.db.session.query(Coterie).get(coterie_id)
    if coterie is not None and coterie.has_partage(get_jwt_identity(), False):
        return jsonify(events=coterie.get_events(min(limit, 100), offset, abs(last_time), 'revert' in request.url_rule.rule)), 200
    return jsonify(message='Autorisation requise'), 401

@webapp.route('/api/events/<int:event_id>', methods=('DELETE',))
@user_jwt_check
def delete_user_event(event_id):
    event = sg.db.new_session().query(Event).get(event_id)
    user = sg.db.session.query(User).get(get_jwt_identity())
    if event is not None and user is not None and event.owner_id == user.id:
        for p in user.partages:
            for h in p.coterie.hooks:
                if h.last_event_id == event.id:
                    h.last_event_id = sg.db.session.query(Event.id).filter(Event.id < h.last_event_id).order_by(Event.id.desc()).first()
                    sg.db.upsert(h)
        sg.db.delete(event)
        return jsonify(message='Événement supprimé !'), 200
    return jsonify(message='Autorisation requise'), 401

# HOOKS
@webapp.route('/api/hook/renew/<int:id>', methods=('POST',))
@user_jwt_check
def renew(id):
    hook = sg.db.session.query(Hook).get(id)
    if hook.coterie.has_partage(get_jwt_identity(), True):
        hook.jwt = create_access_token(identity=hook, expires_delta=False)
        sg.db.upsert(hook)
        return jsonify(message='Hook renouvelé'), 200
    return jsonify(message='Autorisation requise'), 401

@webapp.route('/api/hook/request', methods=('POST',))
@hook_jwt_check
def make_hook_request():
    hook = sg.db.session.query(Hook).get(get_jwt_identity())
    if hook is not None:
        data = request.get_json()
        if 'req' not in data:
            return jsonify(message='Une erreur est survenue...'), 400
        res = sg.req.request(hook.coterie, data.get('req'))
        return jsonify(message=res), 200
    return jsonify(message='Autorisation requise'), 401

@webapp.route('/api/user/request', methods=('POST',))
@user_jwt_check
def make_user_request():
    user = sg.db.session.query(User).get(get_jwt_identity())
    data = request.get_json()
    if 'req' not in data:
        return jsonify(message='Une erreur est survenue...'), 400
    res = sg.req.request(user, data.get('req'))
    return jsonify(message=res), 200

@webapp.route('/api/hook/events', methods=('GET',))
@hook_jwt_check
def get_hook_events():
    hook = sg.db.session.query(Hook).get(get_jwt_identity())
    if hook is not None:
        return jsonify(events=hook.trigger()), 200
    return jsonify(message='Autorisation requise'), 401

@webapp.route('/api/hook/format/<int:hook_id>', methods=('GET',))
@user_jwt_check
def get_hook_format(hook_id):
    hook = sg.db.session.query(Hook).get(hook_id)
    if hook is not None and hook.coterie.has_partage(get_jwt_identity(), True):
        format = Hook.format2ui(hook.format) if hook.format is not None else Hook.format2ui(sg.format)
        return jsonify(format=json.dumps(format)), 200
    return jsonify(message='Autorisation requise'), 401

@webapp.route('/api/hook/format/<int:hook_id>', methods=('POST',))
@user_jwt_check
def set_hook_format(hook_id):
    hook = sg.db.session.query(Hook).get(hook_id)
    if hook is not None and hook.coterie.has_partage(get_jwt_identity(), True):
        data = request.get_json()
        hook = hook.update_format(**data)
        if hook is None:
            return jsonify(message='Une erreur est survenue...'), 400
        return jsonify(message='Format sauvegardé !'), 200
    return jsonify(message='Autorisation requise'), 401

@webapp.route('/api/hook/format/<int:hook_id>', methods=('DELETE',))
@user_jwt_check
def reset_hook_format(hook_id):
    hook = sg.db.session.query(Hook).get(hook_id)
    if hook is not None and hook.coterie.has_partage(get_jwt_identity(), True):
        hook.format = sg.format
        sg.db.upsert(hook)
        return jsonify(message='Configuration réinitialisée'), 200
    return jsonify(message='Autorisation requise'), 401

# DEFAULT ROUTE (redirect to VueJS client)
@webapp.route('/', defaults={'path': ''})
@webapp.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')