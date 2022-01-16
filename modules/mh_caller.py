#! /usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
from classes.capa_meta import MetaCapa
from classes.being_troll import Troll
from classes.being_troll_private import TrollPrivate
from classes.being_troll_private_capa import TrollPrivateCapa
from classes.being import Being
from classes.being_mob import Mob
from classes.being_mob_meta import MetaMob
from classes.being_mob_private import MobPrivate
from classes.tresor_meta import MetaTresor
from classes.lieu import Lieu
from classes.guilde import Guilde
from classes.tresor import Tresor
from classes.tresor_private import TresorPrivate
from classes.champi import Champi
from classes.champi_private import ChampiPrivate
from classes.user_mh_call import MhCall
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import requests, datetime, re, time
import modules.globals as sg


# CLASS DEFINITION
class MhCaller:

    # Constructor
    def __init__(self):
        self.load_conf()

    # Configuration loader
    def load_conf(self):
        self.spURL = sg.conf[sg.CONF_MH_SECTION][sg.CONF_SP_URL]
        self.spParamID = sg.conf[sg.CONF_MH_SECTION][sg.CONF_SP_ID]
        self.spParamAPIKEY = sg.conf[sg.CONF_MH_SECTION][sg.CONF_SP_APIKEY]
        self.spProfil4 = sg.conf[sg.CONF_MH_SECTION][sg.CONF_SP_PROFIL4]
        self.spVue2 = sg.conf[sg.CONF_MH_SECTION][sg.CONF_SP_VUE2]
        self.spParamTresors = sg.conf[sg.CONF_MH_SECTION][sg.CONF_SP_VUE2_TRESORS]
        self.spParamChampis = sg.conf[sg.CONF_MH_SECTION][sg.CONF_SP_VUE2_CHAMPIS]
        self.spParamLieux = sg.conf[sg.CONF_MH_SECTION][sg.CONF_SP_VUE2_LIEUX]
        self.ftpURL = sg.conf[sg.CONF_MH_SECTION][sg.CONF_FTP_URL]
        self.ftpTrolls2 = sg.conf[sg.CONF_MH_SECTION][sg.CONF_FTP_TROLLS2]
        self.ftpMonstres = sg.conf[sg.CONF_MH_SECTION][sg.CONF_FTP_MONSTRES]
        self.ftpTresors = sg.conf[sg.CONF_MH_SECTION][sg.CONF_FTP_TRESORS]
        self.ftpSorts = sg.conf[sg.CONF_MH_SECTION][sg.CONF_FTP_SORTS]
        self.ftpComps = sg.conf[sg.CONF_MH_SECTION][sg.CONF_FTP_COMPS]
        self.ftpGuildes = sg.conf[sg.CONF_MH_SECTION][sg.CONF_FTP_GUILDES]
        self.ftpEvents = sg.conf[sg.CONF_MH_SECTION][sg.CONF_FTP_EVENTS]

    # Main MH caller (should never be a show-stopper, if MH is down for example)
    def call(self, user, scripts, verbose=False, manual=False):
        if scripts is None:
            scripts = ['profil4', 'vue2']
        res = True
        for script in scripts:
            try:
                mh_callable = getattr(self, script + '_sp_call')
                res &= mh_callable(user, verbose, manual)
            except Exception as e:
                sg.logger.warning('Error while calling script %s: %s' % (script, e))
                sg.logger.exception(e)
                sg.db.session.rollback()
        return res

    # Caller to MH Trolls2 FTP
    # See http://ftp.mountyhall.com/help.txt
    def trolls2_ftp_call(self):
        sg.logger.info('Calling trolls2 MH FTP...')
        # Get the file
        sep = ';'
        mh_r = requests.get('http://%s/%s' % (self.ftpURL, self.ftpTrolls2))
        lines = mh_r.text.split('\n')
        trolls = []
        i = 0
        for line in lines:
            if line.count(sep) == 15: # Some lines are wrongly formated
                # Get the data for each troll
                troll = Troll()
                troll.id, troll.nom, troll.race, troll.niv, troll.nb_kill, troll.nb_mort, troll.nb_mouche, troll.guilde_id,\
                troll.guilde_rang, troll.etat, troll.intangible, troll.pnj, troll.ami_mh, troll.inscription_date,\
                troll.blason_uri, empty = line.split(sep)
                # Fix the data
                if not troll.inscription_date:
                    troll.inscription_date = None
                troll.guilde_id = None
                troll.etat = None
                troll.intangible = troll.intangible != '0'
                troll.ami_mh = troll.ami_mh != '0'
                troll.pnj = troll.pnj != '0'
                if troll.blason_uri == 'http://www.mountyhall.com/images/Blasons/Blason_PJ/' + troll.id:
                    troll.blason_uri = 'http://blason.mountyhall.com/Blason_PJ/' + troll.id
                trolls.append(troll)
                i += 1
                if i % 100 == 0:
                    time.sleep(0.1)
        # Separate existing and new objects
        existing = [str(r.id) for r in sg.db.session.query(Troll.id).filter(Troll.id.in_([troll.id for troll in trolls])).all()]
        to_insert = [troll for troll in trolls if str(troll.id) not in existing]
        to_update = [troll for troll in trolls if str(troll.id) in existing]
        # Bulk insert new objects
        if len(to_insert) > 0:
            sg.db.engine.execute(Being.__table__.insert(), [sg.row2dict(Being(id=troll.id, nom=troll.nom, type='Trõll')) for troll in to_insert])
            sg.db.engine.execute(Troll.__table__.insert(), [sg.row2dict(troll) for troll in to_insert])
        # Bulk update old objects
        if len(to_update) > 0:
            session = sg.db.new_session()
            session.bulk_update_mappings(Troll, [sg.row2dictWithoutNone(troll) for troll in to_update])
            session.commit()
            session.close()

    # Caller to the MH Monstres FTP
    # See http://ftp.mountyhall.com/help.txt
    def monstres_ftp_call(self):
        sg.logger.info('Calling monstres MH FTP...')
        # Get the file
        sep = ';'
        mh_r = requests.get('http://%s/%s' % (self.ftpURL, self.ftpMonstres))
        lines = mh_r.text.split('\n')
        session = sg.db.new_session()
        for line in lines:
            if line.count(sep) > 0:
                # Get the data for each mob_meta
                metamob = MetaMob()
                metamob.id, metamob.nom, metamob.determinant, metamob.blason_uri, empty = line.split(sep)
                # Upsert the troll
                sg.db.upsert(metamob, session)
        # Some data are missing...
        missing_mobs = [
            {'id': -1, 'nom': 'Diablotin', 'determinant': 'un', 'blason_uri': 'http://www.mountyhall.com/images/Monstres/Diablotin.jpg'},
            {'id': -2, 'nom': 'Pseudo-Dragon', 'determinant': 'un', 'blason_uri': 'http://www.mountyhall.com/images/Monstres/OF_PseudoDragon.jpg'},
            {'id': -3, 'nom': 'Zombi', 'determinant': 'un', 'blason_uri': 'http://www.mountyhall.com/images/Monstres/Zombi.jpg'},
            {'id': -4, 'nom': 'Essaim Cratérien', 'determinant': 'un', 'blason_uri': '-'},
            {'id': -5, 'nom': 'Gowap', 'determinant': 'un', 'blason_uri': 'http://www.mountyhall.com/images/Monstres/BO_Gowap.jpg'},
            {'id': -6, 'nom': 'Ver Carnivore', 'determinant': 'un', 'blason_uri': 'http://www.mountyhall.com/images/Monstres/GO_Vcg.jpg'},
            {'id': -7, 'nom': 'Familier', 'determinant': 'un', 'blason_uri': '-'},
            {'id': -8, 'nom': 'Gnu', 'determinant': 'un', 'blason_uri': 'http://www.mountyhall.com/images/Monstres/GnuSauvage.jpg'}
        ]
        for missing_mob in missing_mobs:
            metamob = MetaMob()
            for key in missing_mob:
                setattr(metamob, key, missing_mob[key])
            sg.db.upsert(metamob, session)
        session.commit()
        session.close()

    # Caller to the MH Tresors FTP
    # See http://ftp.mountyhall.com/help.txt
    def tresors_ftp_call(self):
        sg.logger.info('Calling tresors MH FTP...')
        # Get the file
        sep = ';'
        mh_r = requests.get('http://%s/%s' % (self.ftpURL, self.ftpTresors))
        lines = mh_r.text.split('\n')
        session = sg.db.new_session()
        for line in lines:
            if line.count(sep) > 0:
                # Get the data for each tresor_meta
                metatresor = MetaTresor()
                metatresor.id, metatresor.nom, metatresor.type, empty = line.split(sep)
                # Fix the data
                metatresor.nom = re.sub('\s*:\s*$', '', metatresor.nom)
                # Upsert the troll
                sg.db.upsert(metatresor, session)
        session.commit()

    # Caller to the MH Sorts/Competences FTP
    # See http://ftp.mountyhall.com/help.txt
    def capas_ftp_call(self):
        # Fetch MH Sorts from FTP
        sg.logger.info('Calling Sorts MH FTP...')
        sep = ';'
        mh_r = requests.get('http://%s/%s' % (self.ftpURL, self.ftpSorts))
        lines = mh_r.text.split('\n')
        session = sg.db.new_session()
        for line in lines:
            if line.find(sep) > 0:
                meta_id, meta_nom, meta_subtype, meta_pa, meta_duree, meta_rm, meta_surface, meta_zone, empty = line.split(sep)
                metacapa = MetaCapa(id=meta_id, nom=meta_nom, type='Sortilège', subtype=meta_subtype, pa=meta_pa)
                sg.db.upsert(metacapa, session)
        session.commit()
        session.close()
        # Fetch MH Comps (Metacapas) from FTP
        sg.logger.info('Calling Comps MH FTP...')
        sep = ';'
        mh_r = requests.get('http://%s/%s' % (self.ftpURL, self.ftpComps))
        lines = mh_r.text.split('\n')
        session = sg.db.new_session()
        for line in lines:
            if line.find(sep) > 0:
                meta_id, meta_nom, meta_subtype, meta_pa, meta_pourcentage_base, meta_niv_min, empty = line.split(sep)
                metacapa = MetaCapa(id='-' + meta_id, nom=meta_nom, type='Compétence', subtype=meta_subtype, pa=meta_pa)
                sg.db.upsert(metacapa, session)
        # Some data are missing...
        missing_capas = [
            {'id': 1001, 'nom': 'Projectile Magique', 'type': 'Sortilège', 'subtype': 'Attaque', 'pa': 4},
            {'id': 1002, 'nom': 'Rafale Psychique', 'type': 'Sortilège', 'subtype': 'Attaque', 'pa': 4},
            {'id': 1003, 'nom': 'Hypnotisme', 'type': 'Sortilège', 'subtype': 'Attaque', 'pa': 4},
            {'id': 1004, 'nom': 'Vampirisme', 'type': 'Sortilège', 'subtype': 'Attaque', 'pa': 4},
            {'id': 1005, 'nom': 'Siphon des âmes', 'type': 'Sortilège', 'subtype': 'Attaque', 'pa': 4},
        ]
        for missing_capa in missing_capas:
            metacapa = MetaCapa()
            for key in missing_capa:
                setattr(metacapa, key, missing_capa[key])
            sg.db.upsert(metacapa, session)
        session.commit()
        session.close()

    # Caller to the Profil4 SP
    def profil4_sp_call(self, user, verbose=False, manual=False):
        sg.logger.info('Calling profil4 for user %s' % user.id)
        now = datetime.datetime.now()
        # Fetch the data from MH
        mh_r = requests.get('http://%s/%s?%s=%s&%s=%s' % (self.spURL, self.spProfil4, self.spParamID, user.id, self.spParamAPIKEY, user.mh_api_key))
        mh_call = MhCall(user_id=user.id, nom='Profil4', type='Dynamique', time=now, status=0, manual=manual)
        # Check for error
        if mh_r.status_code != 200:
            sg.logger.warning('Could not request profil4 for user %s, got HTTP code %d' % (user.id, mh_r.status_code,))
            mh_call.status = 4
            sg.db.upsert(mh_call)
            return False
        res = re.search(r'Erreur\s+(\d)', mh_r.text)
        if res is not None:
            mh_call.status = res.group(1)
            sg.db.upsert(mh_call)
            sg.logger.warning('Error %s while calling profil4 for user %s' % (mh_call.status, user.id))
            if mh_call.status == '6' or mh_call.status == '2':
                sg.logger.warning('MH account for user %s is deactivated, setting SP limits to 0 and disabling hook propagation' % (user.id,))
                user.max_mh_sp_static = user.max_mh_sp_dynamic = 0
                for p in user.partages:
                    p.disablePropagation()
                    sg.db.upsert(p)
                sg.db.upsert(user)
            if verbose:
                print('Erreur lors de la mise à jour du troll n°%s' % user.id)
            return False
        # Parse the data
        sg.db.upsert(mh_call)
        data = mh_r.json()
        # Troll
        troll = Troll()
        troll.id = data['troll']['id']
        troll.nom = data['troll']['nom']
        troll.niv = data['troll']['niveau']
        troll.race = data['troll']['race']
        troll.guilde_id = data['troll']['guilde']
        sg.db.upsert(troll)
        # TrollPrivate
        troll_private = TrollPrivate()
        troll_private.troll_id = troll_private.viewer_id = data['troll']['id']
        troll_private.pi = data['troll']['piTotaux']
        troll_private.pi_disp = data['troll']['piDispo']
        troll_private.pos_x = data['situation']['x']
        troll_private.pos_y = data['situation']['y']
        troll_private.pos_n = data['situation']['n']
        # data['situation']['ph'] ?
        troll_private.pa = data['situation']['pa']
        troll_private.next_dla = datetime.datetime.fromtimestamp(data['situation']['dla']).strftime('%Y-%m-%d %H:%M:%S')
        troll_private.malus_arm = data['situation']['nbTouche']
        troll_private.fatigue = data['situation']['fatigue']['CAR'] + data['situation']['fatigue']['BM']
        troll_private.camouflage = data['situation']['camouflage']
        troll_private.invisible = data['situation']['invisible']
        troll_private.intangible = data['situation']['intangible']
        troll_private.nb_parade_prog = data['situation']['nbParades']
        troll_private.nb_ctr_att_prog = data['situation']['nbCA']
        troll_private.nb_att_sub = data['situation']['nbEsq']
        troll_private.immobile = data['situation']['glue']
        troll_private.terre = data['situation']['aTerre']
        troll_private.course = data['situation']['course']
        troll_private.levite = data['situation']['levitation']
        troll_private.nb_retraite_prog = data['situation']['nbRetraites']
        troll_private.dir_retraite_prog = data['situation']['dirRetraites']
        troll_private.base_tour_min = troll_private.base_tour_max = data['situation']['dureeTour']
        # data['situation']['vueHMax'] ?
        troll_private.base_att_min = troll_private.base_att_max = data['caracs']['att']['CAR']
        troll_private.bonus_att_phy = data['caracs']['att']['BMP']
        troll_private.bonus_att_mag = data['caracs']['att']['BMM']
        troll_private.base_esq_min = troll_private.base_esq_max = data['caracs']['esq']['CAR']
        troll_private.bonus_esq_phy = data['caracs']['esq']['BMP']
        troll_private.bonus_esq_mag = data['caracs']['esq']['BMM']
        troll_private.base_deg_min = troll_private.base_deg_max = data['caracs']['deg']['CAR']
        troll_private.bonus_deg_phy = data['caracs']['deg']['BMP']
        troll_private.bonus_deg_mag = data['caracs']['deg']['BMM']
        troll_private.base_reg_min = troll_private.base_reg_max = data['caracs']['reg']['CAR']
        troll_private.bonus_reg_phy = data['caracs']['reg']['BMP']
        troll_private.bonus_reg_mag = data['caracs']['reg']['BMM']
        troll_private.base_pdv_min = troll_private.base_pdv_max = data['caracs']['pvMax']['CAR']
        troll_private.bonus_pdv_phy = data['caracs']['pvMax']['BMP']
        troll_private.bonus_pdv_mag = data['caracs']['pvMax']['BMM']
        troll_private.pdv = data['caracs']['pvActuels']['CAR']
        # data['caracs']['pvActuels']['BMP']
        # data['caracs']['pvActuels']['BMM']
        troll_private.base_vue_min = troll_private.base_vue_max = data['caracs']['vue']['CAR']
        troll_private.bonus_vue_phy = data['caracs']['vue']['BMP']
        troll_private.bonus_vue_mag = data['caracs']['vue']['BMM']
        troll_private.base_rm_min = troll_private.base_rm_max = data['caracs']['rm']['CAR']
        troll_private.bonus_rm_phy = data['caracs']['rm']['BMP']
        troll_private.bonus_rm_mag = data['caracs']['rm']['BMM']
        troll_private.base_mm_min = troll_private.base_mm_max = data['caracs']['mm']['CAR']
        troll_private.bonus_mm_phy = data['caracs']['mm']['BMP']
        troll_private.bonus_mm_mag = data['caracs']['mm']['BMM']
        troll_private.base_arm_min = troll_private.base_arm_max = data['caracs']['arm']['CAR']
        troll_private.bonus_arm_phy = data['caracs']['arm']['BMP']
        troll_private.bonus_arm_mag = data['caracs']['arm']['BMM']
        troll_private.base_tour_min = troll_private.base_tour_max = data['caracs']['dla']['CAR']
        troll_private.bonus_tour_phy = data['caracs']['dla']['BMP']
        troll_private.bonus_tour_mag = data['caracs']['dla']['BMM']
        # data['caracs']['poids']['CAR']
        troll_private.malus_poids_phy = data['caracs']['poids']['BMP']
        troll_private.malus_poids_mag = data['caracs']['poids']['BMM']
        troll_private.base_concentration = data['caracs']['concentration']['CAR']
        troll_private.bonus_concentration_phy = data['caracs']['concentration']['BMP']
        troll_private.bonus_concentration_mag = data['caracs']['concentration']['BMM']
        troll_private.last_sp4_update_at = now
        troll_private.last_sp4_update_by = user.id
        troll_private.last_seen_at = now
        troll_private.last_seen_by = user.id
        troll_private.last_seen_with = 'SP4'
        sg.db.upsert(troll_private)
        # Compétences et sort
        session = sg.db.new_session()
        for capa in data['competences'] + data['sorts']:
            try:
                metacapa = session.query(MetaCapa).filter(MetaCapa.nom == capa['nom']).one()
                n = 1
                for percent in capa['niveaux']:
                    sub = None if not 'types' in capa or len(capa['types']) < 1 else capa['types'][n-1]
                    try:
                        if sub is None:
                            troll_private_capa = session.query(TrollPrivateCapa).filter(TrollPrivateCapa.metacapa_id == metacapa.id, TrollPrivateCapa.troll_id == user.id, TrollPrivateCapa.niv == n, TrollPrivateCapa.subtype == sub, TrollPrivateCapa.viewer_id == user.id).one()
                        else:
                            troll_private_capa = session.query(TrollPrivateCapa).filter(TrollPrivateCapa.metacapa_id == metacapa.id, TrollPrivateCapa.troll_id == user.id, TrollPrivateCapa.niv == n, TrollPrivateCapa.viewer_id == user.id).one()
                    except (NoResultFound, MultipleResultsFound):
                        troll_private_capa = TrollPrivateCapa()
                    troll_private_capa.troll_id = troll_private_capa.viewer_id = user.id
                    troll_private_capa.metacapa_id = metacapa.id
                    troll_private_capa.niv = n
                    troll_private_capa.percent = percent
                    troll_private_capa.subtype = sub
                    troll_private_capa.bonus = capa['bonus']
                    n += 1
                    sg.db.upsert(troll_private_capa, session)
            except (NoResultFound, MultipleResultsFound):
                sg.logger.warning("Unknown capa '%s' retrieved from MH while upadating troll %s" % (capa['nom'], user.id))
        session.commit()
        session.close()
        if verbose:
            print('Troll n°%s mis à jour' % user.id)
        return True

    # Caller to the Vue2 SP
    def vue2_sp_call(self, user, verbose=False, manual=False):
        sg.logger.info('Calling vue2 for user %s' % user.id)
        now = datetime.datetime.now()
        sep = ';'
        # Fetch the data from MH
        mh_r = requests.get('http://%s/%s?%s=%s&%s=%s&%s=1&%s=1&%s=1' % (self.spURL, self.spVue2, self.spParamID, user.id, self.spParamAPIKEY, user.mh_api_key, self.spParamLieux, self.spParamTresors, self.spParamChampis))
        mh_call = MhCall(user_id=user.id, nom='Vue2', type='Dynamique', time=now, status=0, manual=manual)
        # Check for error
        if mh_r.status_code != 200:
            sg.logger.warning('Could not request Vue2 for user %s, got HTTP code %d' % (user.id, mh_r.status_code,))
            mh_call.status = 4
            sg.db.upsert(mh_call)
            return False
        res = re.search(r'Erreur\s+(\d)', mh_r.text)
        if res is not None:
            mh_call.status = res.group(1)
            sg.db.upsert(mh_call)
            sg.logger.warning('Error %s while calling Vue2 for user %s' % (mh_call.status, user.id))
            if mh_call.status == '6' or mh_call.status == '2':
                sg.logger.warning('MH account for user %s is deactivated, setting SP limits to 0 and disabling hook propagation' % (user.id,))
                user.max_mh_sp_static = user.max_mh_sp_dynamic = 0
                for p in user.partages:
                    p.disablePropagation()
                    sg.db.upsert(p)
                sg.db.upsert(user)
            if verbose:
                print('Erreur lors de la mise à jour de la vue du troll n°%s' % user.id)
            return False
        sg.db.upsert(mh_call)
        # Parse the data
        lines = mh_r.text.split('\n')
        flag = 0 # 1 is Troll, 2 is Mob, 3 is Orig, 4 is Lieux
        objs_set = None
        for line in lines:
            # BULK INSERT/UPDATE
            if line.startswith('#') and objs_set is not None:
                for cls in objs_set:
                    # Separate existing and new objects
                    if cls in [Mob, Troll, Tresor, Champi, Lieu]: # Not a private
                        existing = [str(r.id) for r in sg.db.session.query(cls.id).filter(cls.id.in_([obj.id for obj in objs_set[cls]])).all()]
                        to_insert = [obj for obj in objs_set[cls] if obj.id not in existing]
                        to_update = [obj for obj in objs_set[cls] if obj.id in existing]
                    else:
                        attr_id = 'owner_id'
                        if cls is TrollPrivate: attr_id = 'troll_id'
                        if cls is MobPrivate: attr_id = 'mob_id'
                        if cls is TresorPrivate: attr_id = 'tresor_id'
                        if cls is ChampiPrivate: attr_id = 'champi_id'
                        existing = [str(getattr(r, attr_id)) for r in sg.db.session.query(getattr(cls, attr_id)).filter(getattr(cls, attr_id).in_([getattr(obj, attr_id) for obj in objs_set[cls]]), cls.viewer_id == user.id).all()]
                        to_insert = [obj for obj in objs_set[cls] if str(getattr(obj, attr_id)) not in existing]
                        to_update = [obj for obj in objs_set[cls] if str(getattr(obj, attr_id)) in existing]
                    # Bulk insert new objects
                    if len(to_insert) > 0:
                        if cls is Troll:
                            sg.db.engine.execute(Being.__table__.insert(), [sg.row2dict(Being(id=obj.id, type='Trõll')) for obj in to_insert])
                        if cls is Mob:
                            sg.db.engine.execute(Being.__table__.insert(), [sg.row2dict(Being(id=obj.id, nom=obj.nom, type='Monstre')) for obj in to_insert])
                        sg.db.engine.execute(cls.__table__.insert(), [sg.row2dict(obj) for obj in to_insert])
                    # Bulk update old objects
                    if len(to_update) > 0:
                        session = sg.db.new_session()
                        session.bulk_update_mappings(cls, [sg.row2dictWithoutNone(obj) for obj in to_update])
                        session.commit()
                        session.close()
                objs_set = None
            # PARSING
            if line.upper() == '#DEBUT TROLLS':
                flag, objs_set = 1, {Troll: [], TrollPrivate: []}
            elif line.upper() == '#DEBUT MONSTRES':
                flag, objs_set = 2, {Mob: [], MobPrivate: []}
            elif line.upper() == '#DEBUT ORIGINE':
                flag, objs_set = 3, {TrollPrivate: []}
            elif line.upper() == '#DEBUT LIEUX':
                flag, objs_set = 4, {Lieu: []}
            elif line.upper() == '#DEBUT TRESORS':
                flag, objs_set = 5, {Tresor: [], TresorPrivate: []}
            elif line.upper() == '#DEBUT CHAMPIGNONS':
                flag, objs_set = 6, {Champi: [], ChampiPrivate: []}
            elif not line.startswith('#') and line is not None and line != '':
                if flag == 1:
                    troll_id, troll_pos_x, troll_pos_y, troll_pos_n = line.split(sep)
                    troll = Troll(id=troll_id)
                    troll_private = TrollPrivate(troll_id=troll_id, viewer_id=user.id,
                                                 pos_x=troll_pos_x, pos_y=troll_pos_y, pos_n=troll_pos_n,
                                                 last_seen_at=now, last_seen_by=user.id, last_seen_with='SV2')

                    objs_set[Troll].append(troll)
                    objs_set[TrollPrivate].append(troll_private)
                elif flag == 2:
                    mob_id, mob_nom, mob_pos_x, mob_pos_y, mob_pos_n = line.split(sep)
                    mob = Mob(id=mob_id, mort=False)
                    mob.nom, mob.age, mob.tag = Being.parse_name(mob_id, mob_nom)
                    mob_private = MobPrivate(mob_id=mob_id, viewer_id=user.id,
                                             pos_x=mob_pos_x, pos_y=mob_pos_y, pos_n=mob_pos_n,
                                             last_seen_at=now, last_seen_by=user.id, last_seen_with='SV2')
                    objs_set[Mob].append(mob)
                    objs_set[MobPrivate].append(mob_private)
                elif flag == 3:
                    obj, troll_pos_x, troll_pos_y, troll_pos_n = line.split(sep)
                    troll_private = TrollPrivate(troll_id=user.id, viewer_id=user.id,
                                                 pos_x=troll_pos_x, pos_y=troll_pos_y, pos_n=troll_pos_n,
                                                 last_seen_at=now, last_seen_by=user.id, last_seen_with='SV2')
                    objs_set[TrollPrivate].append(troll_private)
                elif flag == 4:
                    try:
                        lieu_id, lieu_nom, lieu_pos_x, lieu_pos_y, lieu_pos_n = line.split(sep) # For some reason theres is places with html entities in the name...
                        lieu = Lieu(id=lieu_id, nom=lieu_nom,
                                    pos_x=lieu_pos_x, pos_y=lieu_pos_y, pos_n=lieu_pos_n,
                                    last_seen_at=now, last_seen_by=user.id, last_seen_with='SV2')
                        objs_set[Lieu].append(lieu)
                    except Exception as e:
                        pass
                elif flag == 5:
                    tresor_id, tresor_type, tresor_pos_x, tresor_pos_y, tresor_pos_n = line.split(sep)
                    tresor = Tresor(id=tresor_id, type=tresor_type)
                    tresor_private = TresorPrivate(tresor_id=tresor_id, viewer_id=user.id,
                                                   pos_x=tresor_pos_x, pos_y=tresor_pos_y, pos_n=tresor_pos_n,
                                                   last_seen_at=now, last_seen_by=user.id, last_seen_with='SV2')
                    objs_set[Tresor].append(tresor)
                    objs_set[TresorPrivate].append(tresor_private)
                elif flag == 6:
                    champi_id, obj, champi_pos_x, champi_pos_y, champi_pos_n = line.split(sep)
                    champi = Champi(id=champi_id)
                    champi_private = ChampiPrivate(champi_id=champi_id, viewer_id=user.id,
                                                   pos_x=champi_pos_x, pos_y=champi_pos_y, pos_n=champi_pos_n,
                                                   last_seen_at=now, last_seen_by=user.id, last_seen_with='SV2')
                    objs_set[Champi].append(champi)
                    objs_set[ChampiPrivate].append(champi_private)
        if verbose:
            print('Vue du troll n°%s mis à jour' % user.id)
        return True

    # Caller to MH Events FTP
    # See http://ftp.mountyhall.com/evenements/
    def events_ftp_call(self):
        sg.logger.info('Calling Morts MH FTP...')
        # Get the file
        sep = ';'
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        mh_r = requests.get('http://%s/%s' % (self.ftpURL, self.ftpEvents.replace('yyyymmdd', yesterday.strftime("%Y%m%d")).replace('yyyy', yesterday.strftime("%Y"))))
        lines = mh_r.text.split('\n')
        mobs = []
        i = 0
        for line in lines:
            if line.count(sep) == 6: # Some lines are wrongly formated
                # Get the data
                time, att_id, att_nom, def_id, def_nom, type, desc = line.split(sep)
                mob = Mob(mort=True)
                mob.id = def_id if (len(def_id) >= 7) else (att_id if (len(att_id) >= 7 and def_id == "0") else None)
                if mob.id is not None and type == "MORT":
                    mobs.append(mob)
        # Separate existing and new objects
        existing = [str(r.id) for r in sg.db.session.query(Mob.id).filter(Mob.id.in_([mob.id for mob in mobs])).all()]
        to_update = [mob for mob in mobs if str(mob.id) in existing]
        # Bulk update old objects
        if len(to_update) > 0:
            session = sg.db.new_session()
            session.bulk_update_mappings(Mob, [sg.row2dictWithoutNone(mob) for mob in to_update])
            session.commit()
            session.close()

    # Caller to MH Guildes FTP
    # See http://ftp.mountyhall.com/help.txt
    def guildes_ftp_call(self):
        sg.logger.info('Calling Guildes MH FTP...')
        # Get the file
        sep = ';'
        mh_r = requests.get('http://%s/%s' % (self.ftpURL, self.ftpGuildes))
        lines = mh_r.text.split('\n')
        guildes = []
        i = 0
        for line in lines:
            if line.count(sep) == 3: # Some lines are wrongly formated
                # Get the data
                guilde_id, guilde_nom, guilde_count, _ = line.split(sep)
                guilde = Guilde(id=guilde_id, nom=guilde_nom, count=guilde_count)
                guildes.append(guilde)
        # Separate existing and new objects
        existing = [str(r.id) for r in sg.db.session.query(Guilde.id).filter(Guilde.id.in_([guilde.id for guilde in guildes])).all()]
        to_insert = [guilde for guilde in guildes if str(guilde.id) not in existing]
        to_update = [guilde for guilde in guildes if str(guilde.id) in existing]
        # Bulk insert new objects
        if len(to_insert) > 0:
            sg.db.engine.execute(Guilde.__table__.insert(), [sg.row2dict(guilde) for guilde in to_insert])
        # Bulk update old objects
        if len(to_update) > 0:
            session = sg.db.new_session()
            session.bulk_update_mappings(Guilde, [sg.row2dictWithoutNone(guilde) for guilde in to_update])
            session.commit()
            session.close()
