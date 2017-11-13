![SCIZ LOGO](web/public/images/sciz-logo-quarter.png)
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

# Limitations connues

A date, SCIZ supporte l'analyse syntaxique :
  * Des Connaissances Des Monstres jusqu'au niveau 4
  * Des rapports de combats simples (Attaque par compétence, Défense, Pouvoirs)
  * Des sortilèges : Hypnotisme, Sacrifice, Vue Troublée, Explosion

SCIZ ne supporte pas (et plante lamentablement):
  * Les notifications comportant une interposition

Le reste des notifications est a priori ignoré.

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

L'interface Web permet à date :
  - de consulter les évènements collectés par SCIZ pour chaque groupe
  - à chaque utilisateur de modifier son profil SCIZ en self-service
  - aux adminsitrateurs de gérer les différents hooks pour les notifications de groupe

Chaque communauté de joueur utilise ses propres canaux de communication pour recueillir les notifications générées par SCIZ, est disponible à date :
  * Un ```plugin``` et exemple de configuration pour [Hangoutsbot](https://github.com/hangoutsbot/hangoutsbot)
  * Un ```plugin``` pour [Miaou](https://github.com/Canop/miaou)

