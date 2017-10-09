INSTALLATION DE SCIZ (DOCKER)
===

# Introduction

Cette documentation est la procédure d'installation de SCIZ sous Docker.

# Hypothèses

Sont à disposition, avec les privilèges suffisant à leur administration :
 - une machine hôte
 - un nom de domaine associé

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

  2. Editer le fichier ```confs/sciz.ini``` et modifier la valeur des variables suivantes :
      - Section db
        - host=mysql_sciz
        - passwd=MYSQL_PASSWORD #(Remplacez DOMAIN_NAME)

  3. Copier l'ensemble des fichiers du dossier ```docker/``` à la racine des sources SCIZ (sans oublier le fichier ```docker/.env```)

  4. Pré-construire SCIZ

    ```
    docker-compose build
    ```

  5. Création du compte Mail SCIZ

  (Remplacez DOMAIN_NAME et PASSWORD)

  Sous Linux / Mac :

  ```
  ./docker/mailserver_setup.sh -c mail_sciz email add sciz@DOMAIN_NAME PASSWORD
  ```

  Sous Windows :

  ```
  docker-compose run --rm -e MAIL_USER=sciz@DOMAIN_NAME -e MAIL_PASS=PASSWORD -ti mail_sciz /bin/sh -c 'echo "$MAIL_USER|$(doveadm pw -s SHA512-CRYPT -u $MAIL_USER -p MAIL_PASS)"' >> docker/mail_sciz_cfg/postfix-accounts.cf
  ```

  6. Démarrage

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

Cas d'usages les plus propables : la machine hôte possède déjà une base de donnée MySQL ou un serveur Mail installé et en fonctionnement.

## Prérequis

  - Créer un utilisateur ```sciz@DOMAIN_NAME``` sur votre serveur mail (un MailDir doit être disponible)
  - Créer une base et un utilisateur ```sciz``` sur votre serveur MySQL

## Première fois

  1. Editer le fichier ```confs/sciz.ini``` et modifier la valeur des variables suivantes :
    - Section \[mail\]
      - maildir_path
    - Section \[db\]
      - host
      - passwd

  2. Copier les fichiers ```docker/Dockerfile``` et ```docker/sciz-crontab``` à la racine des sources SCIZ

  3. Pré-construire SCIZ

  ```
  docker build -t sciz .
  ```

  4. Démarrage

  (Remplacez MAILDIR_PATH)

  ```
  docker run -d -it --name sciz --net=host -v "$(pwd):/sciz" -v "MAILDIR_PATH:/mail" sciz
  ```

  ## Initialisation de SCIZ

  Vérifier le fichier ```sciz.log``` après chacune des commandes suivantes, aucune erreur ne doit être inscrite.

```
      # Création des tables dans la base SCIZ
      docker-compose exec sciz python sciz.py -i

  (FIXME : édition du JSON pour ajout des utilisateurs)

      # Ajout des utilisateurs
      docker-compose exec sciz python sciz.py -u users.json

      # Population initiale des tables
      docker-compose exec sciz python sciz.py -s monstres
      docker-compose exec sciz python sciz.py -s trolls2
      # /!\ Un appel aux SP MH (catégorie dynamique) par utilisateur et par commande /!\
      docker-compose exec sciz python sciz.py -s profil2
      docker-compose exec sciz python sciz.py -s caracts
```
