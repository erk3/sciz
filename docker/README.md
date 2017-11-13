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

  3. Démarrage

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

  - Etre en mesure de créer des utilisateurs sur votre serveur mail (un MailDir doit être disponible) en fonction du contenu du fichier 'postfix-accounts.cf' généré
  - Créer une base et un utilisateur ```sciz``` sur votre serveur MySQL

## Première fois

  1. Copier les fichiers ```docker/Dockerfile``` et ```docker/sciz-crontab``` à la racine des sources SCIZ

  2. Pré-construire SCIZ

  ```
  docker build --build-arg MYSQL_PASSWORD=MonSuperMotDePasse --build-arg JWT_SECRET=MonSuperSecret --build-arg DOMAIN_NAME=domaine.sciz.a.changer -t sciz .
  ```
  N.B : MonSuperMotDePasse et MonSuperSecret sont à remplacer

  N.B² : des arguments de build docker sont également disponibles pour les valeurs suivantes.
    - MAILDIR_PATH
    - MYSQL_HOST
    - MYSL_PORT

  3. Démarrage

  ```
  docker run -d -it --name sciz --net=host -v "logs:/sciz/logs" -v "%MAILDIR_PATH%:/mail" -v "%PF_FILE_DIRNAME%/mail/config" sciz
  ```

  N.B : %MAILDIR_PATH% et %PF_FILE_DIRNAME% est à remplacer

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
  
  # Ajout des utilisateurs à un groupe à créer
  docker-compose exec sciz python sciz.py -u users.json -g group

  # Population initiale des tables
  # /!\ Un appel aux SP MH (catégorie dynamique) par utilisateur et par commande /!\
  docker-compose exec sciz python sciz.py -a
  ```
