'use strict';

var jwt = require('jsonwebtoken');
var config = require('../../config.js');
var DB = require('../services/database.js');

var AdminController = {}

AdminController.addHook = function (req, res) { 
  
  var groupID = (req.body.groupID) ? parseInt(req.body.groupID) : 0;
  var data = {
    name: req.body.name,
    group_id: groupID,
    jwt: null, // this is created by a Sequelize hook, see models/hook.js
    revoked: false,
    last_event_id : 0 // A try to set it to real last event ID is done below
  };

  var createHook = function (data) {
    DB.Hook.findOne({where: {name: data.name, group_id: data.group_id}})
      .then(function (hook) {
        if (!hook) {
          DB.Hook.create(data)
            .then(function (result) {
              res.json({success: true});
            })
            .catch(function(error) {
              res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
            });
        } else {
          res.status(400).json({message: 'Ce hook existe déjà !'});
        }
      });
  };

  DB.Event.scope().findOne({where: {group_id: data.groupID},order: [['id', 'DESC']]})
    .then(function (event) {
      data.last_event_id = event.id;
      createHook(data);
    })
    .catch(function(error) {
      createHook(data);
    });

}

AdminController.getHooks = function (req, res) {
  var groupID = (req.query.groupID) ? parseInt(req.query.groupID) : 0;
  DB.Hook.findAll({where: {group_id: groupID, revoked: false}})
    .then(function (hooks) {
      res.json(hooks);
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
}

AdminController.revokeHook = function (req, res) {
  var id = (req.query.id) ? parseInt(req.query.id) : 0;
  var groupID = (req.query.groupID) ? parseInt(req.query.groupID) : 0;
  DB.Hook.update({revoked: true}, {where: {id: id, group_id: groupID}})
    .then(function () {
      res.json({success: true});
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
}

module.exports = AdminController;
