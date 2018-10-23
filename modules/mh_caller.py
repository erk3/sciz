#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import ConfigParser, requests, datetime, re
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from classes.assoc_trolls_capas import AssocTrollsCapas
from classes.troll import TROLL
from classes.mob import MOB
from classes.user import USER
from classes.lieu import LIEU
from classes.metamob import METAMOB
from classes.metatresor import METATRESOR
from classes.metacapa import METACAPA
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
            self.spVue2 = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_SP_VUE2)
            self.spParamLieux = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_SP_VUE2_LIEUX)
            self.ftpURL = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_FTP_URL)
            self.ftpTrolls2 = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_FTP_TROLLS2)
            self.ftpMonstres = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_FTP_MONSTRES)
            self.ftpTresors = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_FTP_TRESORS)
            self.ftpSorts = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_FTP_SORTS)
            self.ftpComps = sg.config.get(sg.CONF_MH_SECTION, sg.CONF_FTP_COMPS)
        except ConfigParser.Error as e:
            sg.logger.error("Fail to load config! (ConfigParser error: %s)" % (str(e), ))
            raise

    # Caller to the Profil4 SP
    def profil4_sp_call(self, user, verbose=False):
        # Fetch the data from MH 
        mh_r = requests.get("http://%s/%s?%s=%s&%s=%s" % (self.spURL, self.spProfil4, self.spParamID, user.id, self.spParamAPIKEY, user.mh_apikey, )) 
        # Parse it
        if "Erreur" in mh_r.text:
            sg.logger.warning('Error while fetching data from MH for user %s...' % (user.id, ))
            if verbose:
                print 'Erreur lors de la mise à jour du troll n°%s' % (user.id, )
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
                # Push it to the DB
                troll.last_mhsp4_call = datetime.datetime.now() 
                troll.last_seen = troll.last_mhsp4_call 
                sg.db.add(troll, False)
                # Compétences et sort
                for capa in data['competences'] + data['sorts']:
                    try:
                        metacapa = sg.db.session.query(METACAPA).filter(METACAPA.nom == capa['nom']).one()
                        n = 1
                        for percent in capa['niveaux']:
                            sub = None if not capa.has_key('types') or len (capa['types']) < 1 else capa['types'][n-1]
                            try:
                                if sub is None:
                                    assoc = sg.db.session.query(AssocTrollsCapas).filter(AssocTrollsCapas.metacapa_id == metacapa.id, AssocTrollsCapas.troll_id == user.id, AssocTrollsCapas.niv == n, AssocTrollsCapas.subtype == sub, AssocTrollsCapas.group_id == troll.group_id).one()
                                else:
                                    assoc = sg.db.session.query(AssocTrollsCapas).filter(AssocTrollsCapas.metacapa_id == metacapa.id, AssocTrollsCapas.troll_id == user.id, AssocTrollsCapas.niv == n, AssocTrollsCapas.group_id == troll.group_id).one()
                            except NoResultFound, MultipleResultsFound:
                                assoc = AssocTrollsCapas()
                            assoc.troll_id = troll.id
                            assoc.metacapa_id = metacapa.id
                            assoc.group_id = troll.group_id
                            assoc.niv = n
                            assoc.percent = percent
                            assoc.subtype = sub
                            assoc.bonus = capa['bonus']
                            n += 1
                            sg.db.add(assoc, False)
                    except NoResultFound, MultipleResultsFound:
                        sg.logger.warning("Unknown capa '%s' retrieved from MH while upadating troll %s" % (capa['nom'], user.id, ))
            sg.db.session.commit()
            if verbose:
                print 'Troll n°%s mis à jour' % (user.id, )

    # Caller to the Trolls2 FTP
    def trolls2_ftp_call(self, trolls):
        # Fetch MH Trolls2 from FTP
        mh_r = requests.get("http://%s/%s" % (self.ftpURL, self.ftpTrolls2, ))
        lines = mh_r.text.split('\n')
        for troll in trolls:
            line = [s for s in lines if s.startswith(str(troll.id) + ';')]
            if line is not None and len(line) > 0:
                id, troll.nom, troll.race, troll.niv, troll.nb_kill, troll.nb_mort, troll.nb_mouche, guilde, troll.rang_guilde, troll.etat, troll.intangible, troll.pnj, troll.ami_mh, troll.inscription, troll.blason_url, empty = line[0].split(';')
                troll.etat = troll.etat != u'1'
                troll.intangible = troll.intangible != u'0'
                troll.ami_mh = troll.ami_mh != u'0'
                troll.pnj = troll.pnj != u'0'
                sg.db.add(troll, False)
        sg.db.session.commit()
    
    # Caller to the Vue2 SP
    def vue2_sp_call(self, user, verbose=False):
        # Fetch the data from MH 
        mh_r = requests.get("http://%s/%s?%s=%s&%s=%s&%s=1" % (self.spURL, self.spVue2, self.spParamID, user.id, self.spParamAPIKEY, user.mh_apikey, self.spParamLieux, )) 
        if "Erreur" in mh_r.text:
            sg.logger.warning('Error while fetching data from MH for user %s...' % (user.id, ))
            if verbose:
                print 'Erreur lors de la mise à jour de la vue du troll n°%s' % (user.id, )
        else:
            lines = mh_r.text.split('\n')
            flag = 0 # 1 is Troll, 2 is Mob, 3 is Orig, 4 is Lieux
            last_seen = datetime.datetime.now() 
            obj = None
            for line in lines:
                if line.upper() == "#DEBUT TROLLS":
                    flag = 1
                elif line.upper() == "#DEBUT MONSTRES":
                    flag = 2
                elif line.upper() == "#DEBUT ORIGINE":
                    flag = 3
                elif line.upper() == "#DEBUT LIEUX":
                    flag = 4
                elif not line.startswith("#") and not line is None and not line == '':
                    if flag == 1:
                        for group in user.groups:
                            troll = TROLL()
                            troll.id, troll.pos_x, troll.pos_y, troll.pos_n = line.split(';')
                            troll.group_id = group.group_id
                            troll.last_seen = last_seen
                            sg.db.add(troll, False)
                    elif flag == 2:
                        for group in user.groups:
                            mob = MOB()
                            mob.id, mob.nom, mob.pos_x, mob.pos_y, mob.pos_n = line.split(';')
                            res = re.search('(((?P<mob_det>une?)\s+)?(?P<mob_name>.+)\s+\[(?P<mob_age>.+)\]\s*(?P<mob_tag>.+)?)(?s)', mob.nom)
                            mob.nom = res.groupdict()['mob_name'].replace('\r', '').replace('\n', '')
                            mob.age = res.groupdict()['mob_age'].replace('\r', '').replace('\n', '')
                            mob.tag = res.groupdict()['mob_tag']
                            if mob.tag:
                                mob.tag = mob.tag.replace('\r', '').replace('\n', '')
                            mob.group_id = group.group_id
                            mob.last_seen = last_seen
                            sg.db.add(mob, False)
                    elif flag == 3:
                        for troll in user.trolls:
                            obj, troll.pos_x, troll.pos_y, troll.pos_n = line.split(';')
                            troll.last_seen = last_seen
                            sg.db.add(troll, False)
                    elif flag == 4:
                        lieu = LIEU()
                        lieu.id, lieu.nom, lieu.pos_x, lieu.pos_y, lieu.pos_n = line.split(';')
                        lieu.last_seen = last_seen
                        sg.db.add(lieu, False)
            sg.db.session.commit()
            if verbose:
                print 'Vue du troll n°%s mis à jour' % (user.id, )
                        
    # Caller to the Monstres FTP
    def monstres_ftp_call(self):
        # Fetch MH Monstres (Metamobs) from FTP
        mh_r = requests.get("http://%s/%s" % (self.ftpURL, self.ftpMonstres, ))
        lines = mh_r.text.split('\n')
        for line in lines:
            if line.find(";") > 0:
                metamob = METAMOB()
                metamob.id, metamob.nom, metamob.determinant, metamob.blason_url, empty = line.split(';')
                sg.db.session.merge(metamob)
        sg.db.session.commit()

    # Caller to the Tresors FTP
    def tresors_ftp_call(self):
        # Fetch MH Tresors (Metatresors) from FTP
        mh_r = requests.get("http://%s/%s" % (self.ftpURL, self.ftpTresors, ))
        lines = mh_r.text.split('\n')
        for line in lines:
            if line.find(";") > 0:
                metatresor = METATRESOR()
                metatresor.id, metatresor.nom, metatresor.type, empty = line.split(';')
                sg.db.session.merge(metatresor)
        sg.db.session.commit()

    # Caller to the Sorts/Comps FTP
    def capas_ftp_call(self):
        # Fetch MH Sorts (Metacapas) from FTP
        mh_r = requests.get("http://%s/%s" % (self.ftpURL, self.ftpSorts, ))
        lines = mh_r.text.split('\n')
        for line in lines:
            if line.find(";") > 0:
                metacapa = METACAPA()
                metacapa.id, metacapa.nom, metacapa.subtype, metacapa.pa, metacapa.duree, metacapa.rm, metacapa.surface, metacapa.zone, empty = line.split(';')
                metacapa.type = u"Sortilège"
                sg.db.session.merge(metacapa)
        # Fetch MH Sorts (Metacapas) from FTP
        mh_r = requests.get("http://%s/%s" % (self.ftpURL, self.ftpComps, ))
        lines = mh_r.text.split('\n')
        for line in lines:
            if line.find(";") > 0:
                metacapa = METACAPA()
                metacapa.id, metacapa.nom, metacapa.subtype, metacapa.pa, metacapa.pourcentage_base, metacapa.niv_min, empty = line.split(';')
                metacapa.id = "-" + metacapa.id
                metacapa.type = u"Compétence"
                sg.db.session.merge(metacapa)
        sg.db.session.commit()

    # Main MH call dispatcher
    def call(self, script, trolls, verbose=False):
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
            sg.logger.info("Calling MH ftp %s..." % (script, ))
            self.trolls2_ftp_call(oTrolls)
        elif script == 'monstres':
            sg.logger.info("Calling MH ftp %s..." % (script, ))
            self.monstres_ftp_call()
        elif script == 'tresors':
            sg.logger.info("Calling MH ftp %s..." % (script, ))
            self.tresors_ftp_call()
        elif script == 'capas':
            sg.logger.info("Calling MH ftp %s (Sorts/Comps)..." % (script, ))
            self.capas_ftp_call()
        elif script == 'profil4':
            for oUser in oUsers:
                sg.logger.info("Calling MH script %s for user %s..." % (script, oUser.id, ))
                self.profil4_sp_call(oUser, verbose)
        elif script == 'vue2':
            for oUser in oUsers:
                sg.logger.info("Calling MH script %s for user %s..." % (script, oUser.id, ))
                self.vue2_sp_call(oUser, verbose)

