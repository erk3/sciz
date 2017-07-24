#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import ConfigParser, requests
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sciz_sql_helper import SQLHelper
from sciz_troll_class import TROLL
from sciz_metamob_class import METAMOB
import sciz_globals as sg

## Mountyhall Caller class for SCIZ
class MHCaller:

    # Constructor
    def __init__(self, config):
        self.config = config
        self.check_conf()
        self.sqlHelper = SQLHelper(config)
    
    # Configuration loader and checker
    def check_conf(self):
        try:
            self.spURL = self.config.get(sg.CONF_MH_SECTION, sg.CONF_SP_URL)
            self.spParamID = self.config.get(sg.CONF_MH_SECTION, sg.CONF_SP_ID)
            self.spParamAPIKEY = self.config.get(sg.CONF_MH_SECTION, sg.CONF_SP_APIKEY)
            self.spProfil2 = self.config.get(sg.CONF_MH_SECTION, sg.CONF_SP_PROFIL2)
            self.spCaract = self.config.get(sg.CONF_MH_SECTION, sg.CONF_SP_CARACT)
            self.ftpURL = self.config.get(sg.CONF_MH_SECTION, sg.CONF_FTP_URL)
            self.ftpTrolls2 = self.config.get(sg.CONF_MH_SECTION, sg.CONF_FTP_TROLLS2)
            self.ftpMonstres = self.config.get(sg.CONF_MH_SECTION, sg.CONF_FTP_MONSTRES)
        except ConfigParser.Error as e:
            print("Fail to load config! (ConfigParser error:" + str(e) + ")")
            raise

    # Caller to the Profil2 SP
    def profil2_sp_call(self, troll):
        if troll.user:
            # Fetch the data from MH 
            mh_r = requests.get("http://%s/%s?%s=%s&%s=%s" % (self.spURL, self.spProfil2, self.spParamID, troll.id, self.spParamAPIKEY, troll.user.mh_apikey, )) 
            # Parse it
            if "Erreur" in mh_r.text:
                print 'Error while fetching data from MH...'
            else:
                id, troll.pos_x, troll.pos_y, troll.pos_n, troll.pv, troll.base_pv_max, troll.pa, troll.dla, troll.base_att, troll.base_esq, troll.base_deg, troll.base_reg, troll.base_vue, troll.bonus_arm_phy, troll.base_mm, troll.base_rm, troll.nb_att_sub, troll.fatigue, troll.camouflage, troll.invisible, troll.intangible, troll.nb_parade_prog, troll.nb_ctr_att_prog, troll.base_tour, troll.bonus_tour, troll.base_arm_phy, troll.malus_base_arm_phy, troll.immobile, troll.terre, troll.course, troll.levite, troll.base_bonus_pv_max, troll.niv, troll.pi, troll.id_guilde, troll.limite_vue, troll.nb_retraite_prog, troll.dir_retraite = mh_r.text.split(';') 
                #FIXME : MH SP error ? I got a ''
                troll.nb_retraite_prog = 0
                # Push it to the DB
                self.sqlHelper.session.add(troll)
                self.sqlHelper.session.commit()

    # Caller to the Caract SP
    def caract_sp_call(self, troll):
        if troll.user:
            # Fetch the data from MH
            mh_r = requests.get("http://%s/%s?%s=%s&%s=%s" % (self.spURL, self.spCaract, self.spParamID, troll.id, self.spParamAPIKEY, troll.user.mh_apikey, )) 
            # Parse it
            if "Erreur" in mh_r.text:
                print 'Error while fetching data from MH...'
            else:
                bmm, bmp, car, null = mh_r.text.split("\n")
                #BMM
                bmm_type, troll.bonus_att_mag, troll.bonus_esq_mag, troll.bonus_deg_mag, troll.bonus_reg_mag, troll.bonus_pv_max_mag, troll.bonus_pv_mag, troll.bonus_vue_mag, troll.bonus_rm_mag, troll.bonus_mm_mag, troll.bonus_arm_mag, troll.bonus_tour_mag, troll.malus_poids_mag, troll.bonus_concentration_mag = bmm.split(';')
                #BMP
                bmp_type, troll.bonus_att_phy, troll.bonus_esq_phy, troll.bonus_deg_phy, troll.bonus_reg_phy, troll.bonus_pv_max_phy, troll.bonus_pv_phy, troll.bonus_vue_phy, troll.bonus_rm_phy, troll.bonus_mm_phy, troll.bonus_arm_phy, troll.bonus_tour_phy, troll.malus_poids_phy, troll.bonus_concentration_phy = bmp.split(';')
                bmp_type, bmp_nb_att, bmp_nb_esq, bmp_nb_deg, bmp_nb_reg, bmp_pv_max, bmp_pv, bmp_nb_vue, bmp_rm, bmp_mm, bmp_arm, bmp_tour, bmp_poids, bmp_con = bmp.split(';')
                #BASE CAR
                car_type, troll.base_att, troll.base_esq, troll.base_deg, troll.base_reg, troll.base_pv_max, troll.base_pv, troll.base_vue, troll.base_rm, troll.base_mm, troll.base_arm_phy, troll.base_tour, troll.base_poids, troll.base_concentration = car.split(';')
                # Push it to the DB
                self.sqlHelper.session.add(troll)
                self.sqlHelper.session.commit()
            

    # Caller to the Trolls2 FTP
    def trolls2_ftp_call(self, trolls):
        # Fetch MH Trolls2 from FTP
        mh_r = requests.get("http://%s/%s" % (self.ftpURL, self.ftpTrolls2, ))
        lines = mh_r.text.split('\n')
        for troll in trolls:
            line = [s for s in lines if str(troll.id) in s]
            id, troll.nom, troll.race, troll.niv, troll.nb_kill, troll.nb_mort, troll.nb_mouche, troll.id_guilde, troll.rang_guilde, troll.etat, troll.intangible, troll.pnj, troll.ami_mh, troll.inscription, troll.blason_url, empty = line[0].split(';')
            self.sqlHelper.session.add(troll)
            self.sqlHelper.session.commit()
    
    # Caller to the Monstres FTP
    def monstres_ftp_call(self):
        # Fetch MH Monstres (Metamobs) from FTP
        mh_r = requests.get("http://%s/%s" % (self.ftpURL, self.ftpMonstres, ))
        lines = mh_r.text.split('\n')
        for line in lines:
            if line.find(";") > 0:
                id, nom, determinant, blason_url, empty = line.split(';')
                try:
                    metamob = self.sqlHelper.session.query(METAMOB).filter(METAMOB.id == id).one()
                except NoResultFound, MultipleResultsFound:
                    metamob = METAMOB()
                metamob.id = id
                metamob. nom = nom
                metamob.determinant = determinant
                metamob.blason_url = blason_url
                self.sqlHelper.session.add(metamob)
        self.sqlHelper.session.commit()

    # Main MH call dispatcher
    def call(self, script, trolls):
        # If a list of trolls is specified, get those, else get them all
        oTrolls = []
        if len(trolls) > 0:
            for troll in trolls:
                try:
                    oTroll = self.sqlHelper.session.query(TROLL).filter(TROLL.id == troll).one()
                    oTrolls.append(oTroll)
                except NoResultFound, MultipleResultsFound:
                    print "No Troll %s found in DB, ignoring..." % (troll,)
        else:
            oTrolls = self.sqlHelper.session.query(TROLL).all()
            
        # Actual calls
        if script == 'trolls2':
            #FIXME : mode verbose / logger
            #print "Calling ftp %s..." % (script, )
            self.trolls2_ftp_call(oTrolls)
        elif script == 'monstres':
            #FIXME : mode verbose / logger
            #print "Calling ftp %s..." % (script, )
            self.monstres_ftp_call()
        elif script == 'profil2':
            for oTroll in oTrolls:
                #FIXME : mode verbose / logger
                #print "Calling script %s for Troll %s..." % (script, oTroll.id,)
                self.profil2_sp_call(oTroll)
        elif script == 'caract':
            for oTroll in oTrolls:
                #FIXME : mode verbose / logger
                #print "Calling script %s for Troll %s..." % (script, oTroll.id,)
                self.caract_sp_call(oTroll)

