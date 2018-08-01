# Plugin Discord pour SCIZ

Un plugin Discord permettant de récupérer à interval régulier les notifications de SCIZ.
 
# Pré-requis

  * Créer un serveur Discord
  * Créer une application Discord (https://discordapp.com/developers/applications/me)
  * Copier le ```Client ID```
  * Créer un bot (section "Bot")
  * Copier le ```Token``` du bot
  * Récupérer le ```Channel ID``` du canal de discussion du bot (Mode développeur, clic-droit sur le canal)
  * Autorisez le bot sur votre serveur Discord : https://discordapp.com/oauth2/authorize?client\_id= `Client ID` &scope=bot

# Configurer le bot

Editer le fichier `conf.ini` et modifier la valeur des variables suivantes :

  * Section \[bot\]
    * token (avec ```Token```)
    * channel_id (avec ```Channel ID```)
  * Section \[sciz\] (voir le [wiki](https://github.com/erk3/sciz/wiki/2.4-Gérer-ses-hooks))
    * hook_url
    * jwt

# Lancer le bot

`
pip3 install -r requirements.txt && python3 discord_sciz_bot.py
`

