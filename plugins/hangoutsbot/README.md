# Plugin hangoutsbot pour SCIZ

Un plugin hangoutsbot permettant de récupérer à interval régulier les notifications de SCIZ.
 
# Installation

  * Installer [hangoutsbot](https://github.com/hangoutsbot/hangoutsbot/blob/master/INSTALL.md)
  * Ajouter ```sciz_events.py``` et ̀ ``sciz_requests.py``` dans le dossier ```hangupsbot/plugins```
  * Ajouter la configuration utile au plugin dans le ```config.json``` du bot (voir exemple)
  * Inviter manuellement le bot dans la conversation paramétrée (conv_title)
  * Redémarrer le bot

# Exemples de notification
  * @02:39:10 ~Tahini <b>DEF</b> -1 (71 PV) (Coup Perforant ; Armure : -4 1T) de Pseudo-Dragon [Novice] (5926155)
  * @08:39:10 ~Tahini <b>DEF CAPA</b> -0 (Spores ; Esquive : -1 | Dégâts : -14 | Régénération : -8 | Vue : -2 1T) de Bouj'Dla Placide [Légendaire] (5793865)
  * @10:16:11 ~Eneth CDM Pseudo-Dragon Cogneur (5922663) : 10%
  * @02:25:55 ~Bac ATT (MORT) -81 sur Momie [Récente] (5932810)
  * @09:27:22 ~Põm³ <b>ATT SACRO</b> sur Marmitte (+34 pour -45)
  
# Exemples de requêtes
  * /sciz req 104126 pos,pv,dla
    * TROLL PõmPõmPõm (104126)
    * X=45 Y=4 N=-31
    * PV 154/175
    * DLA 21:17:30 (2PA) / 07:20:30 
  * /sciz req 5900451
    * MOB Grosse Sorcière [Nouvelle] (5900451)
    * Blessure : 0%
    * Niv 17-20
    * PV 170-200
    * Att 7-10 D6
    * [...]
    * Charme (Attaque | Esquive | Vue) 2T
    * MM 1700-2000
    * RM 900-1200
    * Voir le caché : Non
    * [...]
  * /sciz req 104126 event 2
    * @07:23:14 ~Põm³ ATT -46 sur Ettin [Vétéran] (5895436) (Attaque critique Projectile Magique att 78 resi 10 deg 43 esq 5 sr 53)
    * @17:16:05 ~Põm³ DEF -32 (50 PV) (Attaque Paralysante ; DLA +135 minutes 2T) de Alpha Essaim Sanguinaire [Imago] (5899715) (Attaque att 69 resi 32 deg 48 esq 64 sr 21)
