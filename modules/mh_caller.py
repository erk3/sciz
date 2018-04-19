#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import ConfigParser, requests, datetime
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from classes.troll import TROLL
from classes.user import USER
from classes.metamob import METAMOB
import modules.globals as sg

## Mountyhall Caller class for SCIZ
class MHCaller:

    # Constructor
    def __init__(self):
        self.check_conf()
    
    # Configuration loader and checker
    def check_conf(self):
        try:
            self.spURL = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_SP_URL)
            self.spParamID = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_SP_ID)
            self.spParamAPIKEY = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_SP_APIKEY)
            self.spProfil4 = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_SP_PROFIL4)
            self.ftpURL = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_FTP_URL)
            self.ftpTrolls2 = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_FTP_TROLLS2)
            self.ftpMonstres = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_FTP_MONSTRES)
        except ConfigParser.Error as e:
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise

    # Caller to the Profil4 SP
    def profil4_sp_call(self, user):
        # Fetch the data from MH 
        mh_r = requests.get("http://%s/%s?%s=%s&%s=%s" % (self.spURL, self.spProfil4, self.spParamID, user.id, self.spParamAPIKEY, user.mh_apikey, )) 
        # Parse it
        if "Erreur" in mh_r.text:
            sg.logger.warning('Error while fetching data from MH for user %s...' % (user.id, ))
        else:
            data = mh_r.json()
            for troll in user.trolls:
                # Troll
                troll.id = data['troll']['id']
                troll.niv = data['troll']['niveau']
                troll.id_guilde = data['troll']['guilde']
                troll.pi = data['troll']['piTotaux']
                # Situation
                troll.pos_x = data['situation']['x']
                troll.pos_y = data['situation']['y']
                troll.pos_n = data['situation']['n']
                # data['situation']['ph'] ?
                troll.pa = data['situation']['pa']
                troll.dla = datetime.datetime.fromtimestamp(data['situation']['dla']).strftime('%Y-%m-%d %H:%M:%S')
                troll.malus_base_arm_phy = data['situation']['nbTouche']
                troll.fatigue = data['situation']['fatigue']['CAR'] + data['situation']['fatigue']['BM']
                troll.camouflage = data['situation']['camouflage']
                troll.invisible = data['situation']['invisible']
                troll.intangible = data['situation']['intangible']
                troll.nb_parade_prog = data['situation']['nbParades']
                troll.nb_ctr_att_prog = data['situation']['nbCA']
                troll.nb_att_sub = data['situation']['nbEsq']
                troll.immobile = data['situation']['glue']
                troll.terre = data['situation']['aTerre']
                troll.course = data['situation']['course']
                troll.levite = data['situation']['levitation']
                troll.nb_retraite_prog = data['situation']['nbRetraites']
                troll.dir_retraite = data['situation']['dirRetraites']
                troll.base_tour = data['situation']['dureeTour']
                # data['situation']['vueHMax'] ?
                # Caracs
                troll.base_att = data['caracs']['att']['CAR']
                troll.bonus_att_phy = data['caracs']['att']['BMP']
                troll.bonus_att_mag = data['caracs']['att']['BMM']
                troll.base_esq = data['caracs']['esq']['CAR']
                troll.bonus_esq_phy = data['caracs']['esq']['BMP']
                troll.bonus_esq_mag = data['caracs']['esq']['BMM']
                troll.base_deg = data['caracs']['deg']['CAR']
                troll.bonus_deg_phy = data['caracs']['deg']['BMP']
                troll.bonus_deg_mag = data['caracs']['deg']['BMM']
                troll.base_reg = data['caracs']['reg']['CAR']
                troll.bonus_reg_phy = data['caracs']['reg']['BMP']
                troll.bonus_reg_mag = data['caracs']['reg']['BMM']
                troll.base_pv_max = data['caracs']['pvMax']['CAR']
                troll.bonus_pv_max_phy = data['caracs']['pvMax']['BMP']
                troll.bonus_pv_max_mag = data['caracs']['pvMax']['BMM']
                troll.base_bonus_pv_max = troll.base_pv_max + troll.bonus_pv_max_phy + troll.bonus_pv_max_mag
                troll.pv = data['caracs']['pvActuels']['CAR']
                troll.bonus_pv_phy = data['caracs']['pvActuels']['BMP']
                troll.bonus_pv_mag = data['caracs']['pvActuels']['BMM']
                troll.base_vue = data['caracs']['vue']['CAR']
                troll.bonus_vue_phy = data['caracs']['vue']['BMP']
                troll.bonus_vue_mag = data['caracs']['vue']['BMM']
                troll.base_rm = data['caracs']['rm']['CAR']
                troll.bonus_rm_phy = data['caracs']['rm']['BMP']
                troll.bonus_rm_mag = data['caracs']['rm']['BMM']
                troll.base_mm = data['caracs']['mm']['CAR']
                troll.bonus_mm_phy = data['caracs']['mm']['BMP']
                troll.bonus_mm_mag = data['caracs']['mm']['BMM']
                troll.base_arm_phy = data['caracs']['arm']['CAR']
                troll.bonus_arm_phy = data['caracs']['arm']['BMP']
                troll.bonus_arm_mag = data['caracs']['arm']['BMM'] 
                troll.base_tour = data['caracs']['dla']['CAR'] 
                troll.bonus_tour_phy = data['caracs']['dla']['BMP'] 
                troll.bonus_tour_mag = data['caracs']['dla']['BMM'] 
                troll.base_poids = data['caracs']['poids']['CAR'] 
                troll.malus_poids_phy = data['caracs']['poids']['BMP'] 
                troll.malus_poids_mag = data['caracs']['poids']['BMM'] 
                troll.base_concentration = data['caracs']['concentration']['CAR'] 
                troll.bonus_concentration_phy = data['caracs']['concentration']['BMP'] 
                troll.bonus_concentration_mag = data['caracs']['concentration']['BMM'] 
                # FIXME : ajouter compétences et sorts
                # Push it to the DB
                sg.db.add(troll)

    # Caller to the Trolls2 FTP
    def trolls2_ftp_call(self, trolls):
        # Fetch MH Trolls2 from FTP
        mh_r = requests.get("http://%s/%s" % (self.ftpURL, self.ftpTrolls2, ))
        lines = mh_r.text.split('\n')
        for troll in trolls:
            line = [s for s in lines if str(troll.id) in s]
            if line:
                id, troll.nom, troll.race, troll.niv, troll.nb_kill, troll.nb_mort, troll.nb_mouche, troll.id_guilde, troll.rang_guilde, troll.etat, troll.intangible, troll.pnj, troll.ami_mh, troll.inscription, troll.blason_url, empty = line[0].split(';')
                sg.db.add(troll)
    
    # Caller to the Monstres FTP
    def monstres_ftp_call(self):
        # Fetch MH Monstres (Metamobs) from FTP
        mh_r = requests.get("http://%s/%s" % (self.ftpURL, self.ftpMonstres, ))
        lines = mh_r.text.split('\n')
        for line in lines:
            if line.find(";") > 0:
                id, nom, determinant, blason_url, empty = line.split(';')
                try:
                    metamob = sg.db.session.query(METAMOB).filter(METAMOB.id == id).one()
                except NoResultFound, MultipleResultsFound:
                    metamob = METAMOB()
                metamob.id = id
                metamob.nom = nom
                metamob.determinant = determinant
                metamob.blason_url = blason_url
                sg.db.session.add(metamob)
        sg.db.session.commit()

    # Main MH call dispatcher
    def call(self, script, trolls):
        # If a list of trolls (or users) is specified, get those, else get them all
        oTrolls = []
        oUsers = []
        if len(trolls) > 0:
            for troll in trolls:
                try:
                    oUser = sg.db.session.query(USER).filter(USER.id == troll).one()
                    oUsers.append(oUser)
                    oTroll = sg.db.session.query(TROLL).filter(TROLL.id == troll).all()
                    oTrolls.extend(oTroll)
                except NoResultFound:
                    sg.logger.warning("No Troll %s found in DB, ignoring..." % (troll, ))
        else:
            oTrolls = sg.db.session.query(TROLL).all()
            oUsers = sg.db.session.query(USER).all()
            
        # Actual calls
        if script == 'trolls2':
            sg.logger.info("Calling ftp %s..." % (script, ))
            self.trolls2_ftp_call(oTrolls)
        elif script == 'monstres':
            sg.logger.info("Calling ftp %s..." % (script, ))
            self.monstres_ftp_call()
        elif script == 'profil4':
            for oUser in oUsers:
                sg.logger.info("Calling script %s for user %s..." % (script, oUser.id, ))
                self.profil4_sp_call(oUser)

