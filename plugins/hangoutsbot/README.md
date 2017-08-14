# Plugin hangoutsbot pour SCIZ

Un plugin hangoutsbot permettant de récupérer à interval régulier les notifications de SCIZ.
 
# Installation

  * Installer [hangoutsbot](https://github.com/hangoutsbot/hangoutsbot/blob/master/INSTALL.md)
  * Ajouter ```sciz_events.py``` dans le dossier ```hangupsbot\plugins```
  * Ajouter la configuration utile au plugin dans le ```config.json``` du bot
  * Redémarrer le bot

# Exemples de notification
  * @17:09:37 : CDM Succube des Abysses [Initiale] (5900891) : 0%
  * @15:23:25 : DEF -14 (Attaque critique) Põm³ (104126)
  * @08:21:59 : ATT -64 (Attaque critique mortelle) Elémentaire du Chaos [Initial] (5904164)
  
# Note additionnelle

Le plugin [Spawn](https://github.com/hangoutsbot/hangoutsbot/wiki/Spawn-Plugin) de hangoutsbot peut permettre de passer des commandes au module de requêtage de SCIZ (voir exemple de configuration)
  * /sciz req 104126 pos,pv,dla
    * TROLL PõmPõmPõm (104126)
    * X=45 Y=4 N=-31
    * PV 175/175
    * DLA 02:37:30 (0PA)
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
    * @06:58:17 : COMBAT  (Attaque esquivée parfaitement) : Défenseur Põm³ (104126) esq 58 VS Attaquant Petit Bouj'Dla [Jeune] (5886988) att 23
    * @06:03:07 : COMBAT  (Attaque esquivée) : Défenseur Põm³ (104126) esq 66 VS Attaquant Spectre Corrompu [Naissant] (5899382) att 52
