# Système de Chauve-souris Interdimensionnel pour Zhumains

Une base de données collaborative pour jouer en groupe à [Mountyhall](www.mountyhall.com).

# Fonctionnalités principales

* Décomposition analytique des courriels de notification du jeu transférés par les joueurs
* Consolidation et croisement avec les données disponibles publiquement
* Génération de notifications sur évènements
* Moteur de requêtage des informations collectées et générées
* Interface Zhumain Machine
  
# Limitations connues

A date, SCIZ supporte l'analyse syntaxique :
  * Des Connaissances Des Monstres jusqu'au niveau 3
  * Des rapports de combats simples

# Installation
Voir les [instructions d'installation]()

# Exécuter SCIZ
```python sciz.py -c conf/sciz.ini```

```
usage: sciz.py [-h] [-c CONFIG_FILE] [-t] [-u USERS_FILE] [-i]
               [-s PUBLIC_SCRIPT [troll]] [-r mob/troll ...] [-w] [-n]

Système de Chauve-souris Interdimensionnel pour Zhumains

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --conf CONFIG_FILE
                        specify the .ini configuration file
  -t, --test            instruct SCIZ to test your thing
  -u USERS_FILE, --users USERS_FILE
                        instruct SCIZ to create or update users from JSON
  -i, --init            instruct SCIZ to setup the things
  -s PUBLIC_SCRIPT [troll], --script PUBLIC_SCRIPT [troll]
                        instruct SCIZ to call a MountyHall Public Script / FTP
  -r mob/troll ..., --request mob/troll ...
                        instruct SCIZ to pull internal data
  -w, --walk            instruct SCIZ to walk the mails
  -n, --notify          instruct SCIZ to push the pending notifications

From Põm³ with love
```

# Interagir avec SCIZ

Chaque communauté de joueur utilise ses propres canaux de communication, est disponible à date :
  * Un ```plugin``` et exemple de configuration pour [Hangoutsbot](https://github.com/hangoutsbot/hangoutsbot)
