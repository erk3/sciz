'use strict';

var jwt = require('jsonwebtoken');
var config = require('../../config.js');
var db = require('../services/database.js');
var User = require('../models/user.js');

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
    res.status(404).json({message: 'Identifiant et mot de passes requis !'});
  }
  else {
    var id = req.body.id;
    var pwd = req.body.pwd;
    var potentialUser = {where: {id: id}};

    User.findOne(potentialUser)
      .then(function (user) {
        if (!user) {
          res.status(404).json({message: 'Authentification échouée !'});
        }
        else {
          user.comparePasswords(pwd, function (error, isMatch) {
            if (isMatch && !error) {
              var token = jwt.sign(
                {id: user.id},
                config.keys.secret, 
                {expiresIn: '30m'});
              res.json({
                success: true,
                id: user.id,
                pseudo: user.pseudo,
                token: 'JWT ' + token,
                role: user.role,
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
