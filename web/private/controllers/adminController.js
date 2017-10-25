'use strict';

var jwt = require('jsonwebtoken');
var config = require('../../config.js');
var db = require('../services/database.js');
var User = require('../models/user.js');
var Hook = require('../models/hook.js');

var AdminController = {}

AdminController.addHook = function (req, res) { 
  var data = {
    nom: req.body.nom,
    jwt: null, // this is created by a Sequelize hook, see models/hook.js
    revoked: false,
    last_event_id : 0
  };

  Hook.create(data)
    .then(function (result) {
      res.json({success: true});
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
}

AdminController.getHooks = function (req, res) {
  Hook.findAll({where: {revoked: false}})
    .then(function (hooks) {
      res.json(hooks);
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
}

AdminController.revokeHook = function (req, res) {
  Hook.update({revoked: true}, {where: {id: req.query.id}})
    .then(function () {
      res.json({success: true});
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
}

module.exports = AdminController;
