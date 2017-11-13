INSTALLATION DE SCIZ
===

# Introduction

Cette documentation est la procédure d'installation de SCIZ, elle détaille les nombreuses étapes nécessaires au déploiement d'un nouvel environnement SCIZ.

**L'usage de [docker](docker/README.md) est fortement recommandé** à titre d'alternative.

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

De nombreux serveurs mails peuvent être utilisés, le seul prérequis est l'usage d'un MailDir.
Ci-après un exemple de configuration minimale.

```
apt-get install postfix courier-imap 
```

Sélectionnez l'option "Site Internet" a lors de la configuration du paquet.

Editez ensuite le fichier ```/etc/postfix/main.cf``` et adaptez le à votre configuration réseau.
En particulier :
```
home_mailbox = Maildir/
```

Modifiez ensuite le fichier ```/etc/.procmailrc``̀ :
```
MAILDIR=$HOME/Maildir
DEFAULT=$MAILDIR/

:0:
$DEFAULT
```

Éditez le fichier de configuration de courier-imap ```/etc/courier/imapd```:

```
MAILDIRPATH=Maildir
```

Créez enfin le  Maildir :
 
``̀ 
mkdir ~/Maildir
``̀ 

(La configuration DNS, les enregistrements MX, etc., utiles au routage des mails ne sont pas décrit ici et restent à votre charge)

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
cp docker/sciz-crontab sciz-crontab
# Edit the sciz-crontab and change the HOME environment variable according to your setup
crontab sciz-crontab
```

## Configuration minimale de SCIZ

Editer le fichier ```confs/sciz.ini``` et modifier la valeur des variables suivantes :
    - Section \[mail\]
      - maildirs_base_path
      - postfix_accounts_conf_file
      - domain_name
    - Section \[db\]
      - host
      - port
      - passwd

## Installation de l'environnement Web

L'environnement Web est basé sur NodeJS, il existe différente manière de l'installer. Par exemple :

```
curl -sL https://deb.nodesource.com/setup_8.x | bash -
apt-get install -y nodejs
```

Une fois NodeJS installé :

```
npm -C web install
npm -C web run postinstall
npm -C web run build
```

## Configuration de l'application Web

Editer le fichier ```web/config.js``` et modifier la valeur des variables suivantes :
    - Objet {config.sciz}
      - bin
    - Objet {config.server}
      - port_server
    - Objet {config.db}
      - password
    - Objet {config.db.details}
      - host
      - port
    - Objet {config.keys}
      - secret

## Initialisation de SCIZ

Vérifier le fichier ```sciz.log``` après chacune des commandes suivantes, aucune erreur ne doit être inscrite.

Les commandes sont à éxécuter à la racine des sources SCIZ.

Un exemple de fichier JSON pour l'ajout des utilsateurs est disponible dans le dossier ```examples```

```
# Création des tables dans la base SCIZ
python sciz.py -i

# Ajout des utilisateurs
python sciz.py -u users.json

# Ajout des utilisateurs à un groupe à créer
python sciz.py -u users.json -g group

# Population initiale des tables
# /!\ Un appel aux SP MH (catégorie dynamique) par utilisateur et par commande /!\
python sciz.py -a
```

## Démmarage du serveur Web

```
npm -C web start
```
