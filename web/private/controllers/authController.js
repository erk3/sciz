'use strict';

var jwt = require('jsonwebtoken');
var sequelize = require('sequelize');
var config = require('../../config.js');

var DB = require('../services/database.js');
var AuthController = {};

/*
AuthController.signUp = function(req, res) {
    if(!req.body.id || !req.body.pwd) {
        res.json({ message: 'Please provide a username and a password.' });
    } else {
        db.sync().then(function() {
            var newUser = {
                id: req.body.id,
                pwd: req.body.pwd
            };

            return User.create(newUser).then(function() {
                res.status(201).json({ message: 'Account created!' });
            });
        }).catch(function(error) {
            console.log(error);
            res.status(403).json({ message: 'Username already exists!' });
        });
    }
}
*/

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
              var token = jwt.sign(
                {type: 'user', id: user.id, assocs: user.assocs},
                config.keys.secret, 
                {expiresIn: '30m'});
              var blasonURL = (user.trolls.length > 0) ? user.trolls[0].blason_url : 'images/MyNameIsobody.gif';
              res.json({
                success: true,
                id: user.id,
                pseudo: user.pseudo,
                session_duration: user.session_duration,
                default_group_id: user.default_group_id,
                token: 'JWT ' + token,
                blasonURL: blasonURL,
                assocs: user.assocs
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
