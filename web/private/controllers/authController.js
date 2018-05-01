'use strict';

var jwt = require('jsonwebtoken');
var sequelize = require('sequelize');
var request = require('request');
var config = require('../../config.js');

var DB = require('../services/database.js');
var AuthController = {};

AuthController.signup = function(req, res) {
    if(!req.body.id || !req.body.pwd || req.body.pwd.length < 8 || !req.body.mh_apikey) {
        res.status(404).json({message: 'Formulaire erroné !'});
    } else {
      var id = req.body.id;
      var pseudo = "";
      var pwd = req.body.pwd;
      var mh_apikey = req.body.mh_apikey;
      var potentialUser = {where: {id: id}};
      
      DB.User.findOne(potentialUser)
        .then(function (user) {
          if (user) {
            res.status(404).json({message: 'Cet utilisateur existe déjà !'});
          }
          else {
            // Appel à MH pour vérifier couple id/mh_apikey
            request.get({
              "uri": config.mh.sp + config.mh.profil2Public_path + '?' + config.mh.p_id + '=' + id + '&' + config.mh.p_apikey + '=' + mh_apikey,
              "encoding": "binary"
            },
            (err, resp, body) => {
              if (err || body.indexOf('Erreur') !== -1) {
                res.status(400).json({message: 'Vérification MH impossible, vérifiez votre mot de passe restreint !'});
                return;
              }
              // Get the name of the troll for pseudo
              pseudo = body.split(';')[1];
              // Création de l'utilisateur
              var user = {id: id, pwd: pwd, pseudo: pseudo, mh_apikey: mh_apikey};
              DB.User.create(user)
                .then(function (user) {
                  // Done
                  res.status(200).json({message: 'Utilisateur créé'});
                })
                .catch(function(error) {
                  res.status(500).json({message: 'Une erreur est survenue :' + error.message});
                });
            });
          }
      })
      .catch(function(error) {
        res.status(500).json({message: 'Une erreur est survenue :' + error.message});
      });
    }
}

AuthController.authenticate = function (req, res) {
  if (!req.body.id || !req.body.pwd) {
    res.status(404).json({message: 'Identifiant, mot de passe et groupe requis !'});
  }
  else {
    var id = req.body.id;
    var pwd = req.body.pwd;
    var potentialUser = {where: {id: id}};

    DB.User.findOne(potentialUser)
      .then(function (user) {
        if (!user) {
          res.status(404).json({message: 'Authentification échouée !'});
        }
        else {
          user.comparePasswords(pwd, function (error, isMatch) {
            if (isMatch && !error) {
              var lightAssocs = [];
              for (var i = 0; i < user.assocs.length; i++) {
                lightAssocs.push((({ user_id, group_id, role, pending }) => ({ user_id, group_id, role, pending }))(user.assocs[i]));
              }
              var token = jwt.sign(
                {type: 'user', id: user.id, assocs: lightAssocs},
                config.keys.secret, 
                {expiresIn: '30m'});
              var blasonURL = (user.trolls.length > 0) ? user.trolls[0].blason_url : 'images/MyNameIsobody.gif';
              res.status(200).json({
                success: true,
                id: user.id,
                pseudo: user.pseudo,
                session_duration: user.session_duration,
                default_group_id: user.default_group_id,
                token: 'JWT ' + token,
                blasonURL: blasonURL,
                assocs: user.assocs.filter(assoc => assoc.pending === false)
               });
            }
            else {
              res.status(404).json({message: 'Authentification échouée !'});
            }
          });
        }
      })
      .catch(function(error) {
        res.status(500).json({message: 'Une erreur est survenue :' + error.message});
      });
  }
}

module.exports = AuthController;
