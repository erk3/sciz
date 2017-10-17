INSTALLATION DE SCIZ (DOCKER)
===

# Introduction

Cette documentation est la procédure d'installation de SCIZ sous Docker.

# Hypothèses

Sont à disposition, avec les privilèges suffisant à leur administration :
 - une machine hôte
 - un nom de domaine associé

 (La configuration DNS, les enregistrements MX, etc., utiles au routage des mails ne sont pas décrit ici et restent à votre charge)

# Prérequis

Installation de Docker :

  - [Docker \[Compose\] pour Linux](https://docs.docker.com/engine/installation/linux/)
  - [Docker \[Compose\] pour Windows](https://docs.docker.com/engine/installation/windows/)
  - [Docker \[Compose\] pour Mac OS X](https://docs.docker.com/engine/installation/mac/)

# Déploiement full-stack (conseillé)

## Première fois

  1. Editer le fichier ```docker/.env``` et modifier la valeur des variables suivantes :
    - DOMAIN_NAME
    - MYSQL_ROOT_PASSWORD
    - MYSQL_PASSWORD
    - JWT_SECRET

  2. Copier l'ensemble des fichiers du dossier ```docker/``` à la racine des sources SCIZ (sans oublier le fichier ```docker/.env```)

  3. Pré-construire SCIZ

  ```
  docker-compose build
  ```

  4. Création du compte Mail SCIZ

    Sous Linux / Mac :

  ```
  ./docker/mailserver_setup.sh -c mail_sciz email add sciz@%DOMAIN_NAME% %PASSWORD%
  ```

  Sous Windows :

  ```
  docker-compose run --rm -e MAIL_USER=sciz@%DOMAIN_NAME% -e MAIL_PASS=%PASSWORD% -ti mail_sciz /bin/sh -c 'echo "$MAIL_USER|$(doveadm pw -s SHA512-CRYPT -u $MAIL_USER -p MAIL_PASS)"' >> docker/mail_sciz_cfg/postfix-accounts.cf
  ```

  N.B : %DOMAIN_NAME% et %PASSWORD% sont à remplacer

  5. Démarrage

  ```
  docker-compose up -d
  ```

## Arrêt

  ```
  docker-compose down
  ```

## Second démarrage et suivants

  ```
  docker-compose up -d --build
  ```

## Désinstallation

/!\ Cette commande supprime également l'ensemble des données persistantes /!\

  ```
  docker-compose down --volumes
  ```

# Déploiement unitaire

Cas d'usages les plus probables : la machine hôte possède déjà une base de donnée MySQL et/ou un serveur Mail installés et en fonctionnement.

## Prérequis

  - Créer un utilisateur ```sciz@DOMAIN_NAME``` sur votre serveur mail (un MailDir doit être disponible)
  - Créer une base et un utilisateur ```sciz``` sur votre serveur MySQL

## Première fois

  1. Copier les fichiers ```docker/Dockerfile``` et ```docker/sciz-crontab``` à la racine des sources SCIZ

  2. Pré-construire SCIZ

  ```
  docker build --build-arg MYSQL_PASSWORD=MonSuperMotDePasse --build-arg JWT_SECRET=MonSuperSecret -t sciz .
  ```
  N.B : MonSuperMotDePasse et MonSuperSecret sont à remplacer

  N.B² : des arguments de build docker sont également disponibles les valeurs suivantes.
    - MAILDIR_PATH
    - MYSQL_HOST
    - MYSL_PORT

  3. Démarrage

  ```
  docker run -d -it --name sciz --net=host -v "logs:/sciz/logs" -v "%MAILDIR_PATH%:/mail" sciz
  ```

  N.B : %MAILDIR_PATH% est à remplacer

## Initialisation de SCIZ

  Vérifier le fichier ```sciz.log``` après chacune des commandes suivantes, aucune erreur ne doit être inscrite.

  Les commandes sont à éxécuter à la racine des sources SCIZ.

  Un exemple de fichier JSON pour l'ajout des utilsateurs est disponible dans le dossier ```examples```

  (Les commandes sont fournies dans le cas d'un usage full-stack, remplacez ```docker-compose``` par ```docker``` dans les commandes suivantes et dans le cas d'un usage unitaire)

  ```
  # Création des tables dans la base SCIZ
  docker-compose exec sciz python sciz.py -i

  # Ajout des utilisateurs
  docker-compose exec sciz python sciz.py -u users.json

  # Population initiale des tables
  docker-compose exec sciz python sciz.py -s monstres
  docker-compose exec sciz python sciz.py -s trolls2
  # /!\ Un appel aux SP MH (catégorie dynamique) par utilisateur et par commande /!\
  docker-compose exec sciz python sciz.py -s profil2
  docker-compose exec sciz python sciz.py -s caracts
  ```
