'use strict';

var jwt = require('jsonwebtoken');
var config = require('../../config.js');
var DB = require('../services/database.js');

var UserController = {}

UserController.updateProfile = function (req, res) {
  
  var potentialUser = {where: {id: req.user.id}};

  var data = {
    pseudo: req.body.pseudo,
    mh_apikey: req.body.mh_apikey,
    default_group_id: req.body.default_group_id,
    session_duration: req.body.session_duration,
    dyn_sp_refresh: req.body.dyn_sp_refresh,
    static_sp_refresh: req.body.static_sp_refresh
  };

  var update = function (user, data, res) {
    DB.User.update(data, user)
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
      DB.User.findOne(potentialUser)
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
  
  DB.User.findOne(potentialUser)
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
          session_duration: user.session_duration,
          default_group_id: user.default_group_id,
          dyn_sp_refresh: user.dyn_sp_refresh,
          static_sp_refresh: user.static_sp_refresh,
          trolls: user.trolls,
          assocs: user.assocs,
        });
      }
    })
    .catch(function( error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error});
    });
}

UserController.deleteUser = function (req, res) {
  var potentialUser = {where: {id: req.user.id}};
  
  DB.User.destroy(potentialUser)
    .then(function (user) {
      res.json({success: true});
    })
    .catch(function (error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error});
    });
}

UserController.getUsersList = function (req, res) {
  
  DB.User.scope().findAll({attributes: ['id', 'pseudo']})
    .then(function (users) {
      res.json(users);
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue :' + error.message});
    });
}

module.exports = UserController;
