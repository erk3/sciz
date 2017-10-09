INSTALLATION DE SCIZ
===

# Introduction

Cette documentation est la procédure d'installation de SCIZ, elle détaille les nombreuses étapes nécessaires au déploiement d'un nouvel environnement SCIZ.

L'usage de [docker](docker/README.md) est fortement recommandé à titre d'alternative.

# Hypothèses

Sont à disposition, avec les privilèges suffisant à leur administration :
  - un machine hôte sous distribution Linux
  - un nom de domaine associé

(Documentation existante à date uniquement pour Debian)

# Prérequis

Installation d'outils standards :

    apt-get install build-essential
    apt-get install git

# Installation de MySQL

(FIXME)

# Installation Mail

(FIXME : résultat doit être un MailDir)

# Installation SCIZ

    git clone https://github.com/erk3/sciz.git

## Installation de l'environnement Python

    apt-get install libffi-dev
    apt-get install python2.7

(FIXME : installation pip?)

    pip install -r sciz/requirements.txt


## Installation de la crontab

(FIXME : possibilité de modification fréquence crontab)

    apt-get install cron
    cp sciz/docker/sciz-crontab /etc/cron.d/
    chmod 0644 /etc/cron.d/sciz-crontab

## Configuration de SCIZ

(FIXME : modification de la première section du fichier confs/sciz.ini)

## Initialisation de SCIZ

Vérifier le fichier ```sciz.log``` après chacune des commandes suivantes, aucune erreur ne doit être inscrite.

    cd sciz

    # Création des tables dans la base SCIZ
    python sciz.py -i

(FIXME : édition du JSON pour ajout des utilisateurs)

    # Ajout des utilisateurs
    python sciz.py -u users.json

    # Population initiale des tables
    python sciz.py -s monstres
    python sciz.py -s trolls2
    # /!\ Un appel aux SP MH (catégorie dynamique) par utilisateur et par commande /!\
    python sciz.py -s profil2
    python sciz.py -s caracts
