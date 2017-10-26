'use strict';

var jwt = require('jsonwebtoken');
var config = require('../../config.js');
var db = require('../services/database.js');
var User = require('../models/user.js');

var UserController = {}

UserController.updateProfile = function (req, res) {
  
  var potentialUser = {where: {id: req.body.id}};

  var data = {
    pseudo: req.body.pseudo,
    mh_apikey: req.body.mh_apikey
  };

  var update = function (user, data, res) {
    User.update(data, user)
    .then(function (result) {
      res.json({success: true});
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
  }

  if (!req.body.oldPwd && !req.body.newPwd && !req.body.pwd) {
    update(potentialUser, data, res);
  } else {
    if ((req.body.newPwd.length >= 8) && (req.body.newPwd == req.body.pwd)) {
      User.findOne(potentialUser)
        .then(function (user) {
          if (!user) {
            res.status(400).json({message: 'Profil inexistant !'});
          }
          else {
            user.comparePasswords(req.body.oldPwd, function (error, isMatch) {
              if (isMatch && !error) {
                data.pwd = req.body.newPwd;
                update(potentialUser, data, res);
              }
              else {
                res.status(400).json({message: 'Mauvais mot de passe !'});
              }
          });
        }
      })
      .catch(function(error) {
        res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
      });
    } else {
      res.status(400).json({message: 'Données invalides !'});
    }
  }
};

UserController.getProfile = function (req, res) {
  var potentialUser = {where: {id: req.user.id}};
  
  User.findOne(potentialUser)
    .then(function (user) {
      if (!user) {
        res.status(404).json({message: 'Profil inexistant !'});
      }
      else {
        res.json({
          success: true,
          id: user.id,
          pseudo: user.pseudo,
          mh_apikey: user.mh_apikey,
          nom: user.troll.nom,
          race: user.troll.race,
          blason_url: user.troll.blason_url
        });
      }
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue !'});
    });
}

module.exports = UserController;
