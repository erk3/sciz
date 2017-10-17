INSTALLATION DE SCIZ
===

# Introduction

Cette documentation est la procédure d'installation de SCIZ, elle détaille les nombreuses étapes nécessaires au déploiement d'un nouvel environnement SCIZ.

L'usage de [docker](docker/README.md) est fortement recommandé à titre d'alternative.

# Hypothèses

Sont à disposition, avec les privilèges suffisant à leur administration :
  - un machine hôte sous distribution Linux
  - un nom de domaine associé

(Documentation existante à date uniquement pour Debian, toute aide pour étendre la documentation à d'autres distributions est la bienvenue)

# Prérequis

Installation des outils standards :
```
apt-get install build-essential
apt-get install git
```

# Installation de MySQL (minimal)

## Installation du serveur
```
apt-get install mysql-server
```

(Le mot de passe root que vous serez invité à saisir sera par la suite référencé par MYSQL_ROOT_PASSWORD)

## Configuration du serveur

Le mot de passe MYSQL_PASSWORD pour l'utilisateur sciz est à remplacer.

```
mysql -u root -p MYSQL_ROOT_PASSWORD
> create database sciz;
> create user 'sciz@localhost' identified by 'MYSQL_PASSWORD';
> grant all on sciz.* to 'sciz' identified by 'MYSQL_PASSWORD';
> exit
```

# Installation Mail (minimal)

Il faut dans un premier temps installer postfix et courier-imap:
```
apt-get install postfix courier-imap 
```

Si postfix est déja installé, vous pouvez le reconfigurer via la commande suivante:
```
dpkg-reconfigure postfix
```

Dans l'écran de configuration qui va apparaitre, sélectionnez l'option "Site Internet"

Il vous faut ensuite modifier le fichier de configuration de postfix /etc/postfix/main.cf
Adaptez-le à votre configuration réseau. La ligne suivante:
```
home_mailbox = Maildir/
```
doit être présente dans le vôtre fichier de configuration. Le cas échéant, rajoutez là.
Elle est en effet cruciale au fonctionnement de SCIZ.

Modifiez ensuite le fichier /etc/.procmailrc. Si le fichier n'existe pas , il vous faudra
le créer. Il doit contenir les informations suivantes:
```
MAILDIR=$HOME/Maildir
DEFAULT=$MAILDIR/

:0:
$DEFAULT
```

Éditez le fichier de configuration de courier-imap /etc/courier/imapd:

celui-ci doit contenir la ligne suivante:

```
MAILDIRPATH=Maildir
```

La configuration est maintenant terminée. Placez-vous dans votre répertoire HOME
et entrez la commande suivante:

```
mkdir Maildir
```

Ceci créera la boîte de courriel Maildir/ dans votre HOME qui sera utilisé par SCIZ.

La configuration DNS, les enregistrements MX, etc., utiles au routage des mails ne 
sont pas décrits ici et restent à votre charge.

# Installation SCIZ
```
git clone https://github.com/erk3/sciz.git
```

## Installation de l'environnement Python
```
apt-get install libffi-dev
apt-get install python2.7
apt-get install python-pip
pip install -r sciz/requirements.txt
```

## Installation de la crontab
```
apt-get install cron
cp sciz/docker/sciz-crontab /etc/cron.d/
chmod 0644 /etc/cron.d/sciz-crontab
```

N.B : il est possible ici de modifier les fréquences d'exécution de SCIZ (en particulier, si l'on souhaite réduire les appels au scripts publics de Mountyhall)

## Configuration de SCIZ

Editer le fichier ```confs/sciz.ini``` et modifier la valeur des variables suivantes :
    - Section \[mail\]
      - maildir_path
    - Section \[db\]
      - host
      - passwd

## Initialisation de SCIZ

Vérifier le fichier ```sciz.log``` après chacune des commandes suivantes, aucune erreur ne doit être inscrite.

Les commandes sont à éxécuter à la racine des sources SCIZ.

Un exemple de fichier JSON pour l'ajout des utilsateurs est disponible dans le dossier ```examples```

```
# Création des tables dans la base SCIZ
python sciz.py -i

# Ajout des utilisateurs
python sciz.py -u users.json

# Population initiale des tables
python sciz.py -s monstres
python sciz.py -s trolls2
# /!\ Un appel aux SP MH (catégorie dynamique) par utilisateur et par commande /!\
python sciz.py -s profil2
python sciz.py -s caracts
```
