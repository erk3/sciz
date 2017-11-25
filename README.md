![SCIZ LOGO](web/public/images/sciz-logo-quarter.png)
[![Chat on Miaou](https://dystroy.org/miaou/static/shields/room-fr.svg?v=1)](https://dystroy.org/miaou/2603?SCIZ)
# Système de Chauve-souris Interdimensionnel pour Zhumains

Une base de données collaborative pour jouer en groupe à [Mountyhall](https://www.mountyhall.com).

# Fonctionnalités principales

* Décomposition analytique des courriels de notification du jeu transférés par les joueurs
* Consolidation éventuelle et croisement avec les données disponibles publiquement
* Génération de notifications sur évènements
* Moteur de requêtage des informations collectées et générées
* Interface Zhumain Machine

# Avertissement

SCIZ effectue des appels aux scripts publics de Mountyhall, chaque utilisateur peut modifier ce comportement dans son profil utilisateur via l'interface web.

# Installation
Voir les [instructions d'installation](INSTALL.md)

# Exécuter SCIZ manuellement
```python sciz.py -h```

```
usage: sciz.py [-h] [-c CONFIG_FILE] [-l LOGGING_LEVEL] [-a] [-u USERS_FILE]
               [-r REQUEST_CLI | help] [-w] [-n HOOK_NAME]
               [-s PUBLIC_SCRIPT [troll]] [-i] [-g GROUP_NAME]

Système de Chauve-souris Interdimensionnel pour Zhumains

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --conf CONFIG_FILE
                        specify the .ini configuration file
  -l LOGGING_LEVEL, --logging-level LOGGING_LEVEL
                        specify the level of logging
  -a, --auto            instruct SCIZ to start the recurrent automagic things
  -u USERS_FILE, --users USERS_FILE
                        instruct SCIZ to create or update users from JSON
  -r REQUEST_CLI | help, --request REQUEST_CLI | help
                        instruct SCIZ to pull internal data
  -w, --walk            instruct SCIZ to walk the mails
  -n HOOK_NAME, --notify HOOK_NAME
                        instruct SCIZ to push the pending notifications for a
                        hook
  -s PUBLIC_SCRIPT [troll], --script PUBLIC_SCRIPT [troll]
                        instruct SCIZ to call a MountyHall Public Script / FTP
  -i, --init            instruct SCIZ to setup the things
  -g GROUP_NAME, --group GROUP_NAME
                        set the working group

From Põm³ with love
```

# Interagir avec SCIZ

SCIZ est livré avec une interface Web permettant :
  - de consulter les évènements collectés par SCIZ pour chaque groupe
  - à chaque utilisateur de modifier son profil SCIZ en self-service
  - aux adminsitrateurs de groupe de gérer les différents hooks

Chaque communauté de joueur utilise cependant ses propres canaux de communication pour s'interfacer avec SCIZ par le biais de plugins.

# Aller plus loin...

Consultez le [WIKI](https://github.com/erk3/sciz/wiki)
