'use strict';

var config = require('../../config.js');
var DB = require('../services/database.js');

var PadController = {}

/*
 * Pad
 */
PadController.getPad = function (req, res) {
  var groupID = (req.query.groupID) ? parseInt(req.query.groupID) : 0;
  DB.Pad.find({where: {group_id: groupID}})
    .then(function (pad) {
      res.json(pad);
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
    });
}

PadController.updatePad = function (req, res) {
  var groupID = (req.body.groupID) ? parseInt(req.body.groupID) : 0;
  var pad = (req.body.pad) ? req.body.pad : null;
  
  if (pad === null) {
    res.status(400).json({message: 'Aucunde donnée !'});
  } else {
    var potentialPad = {where: {group_id: groupID}};
    var data = {value: pad};

    DB.Pad.update(data, potentialPad)
      .then(function (result) {
        res.json({success: true});
      })
      .catch(function(error) {
        res.status(500).json({message: 'Une erreur est survenue ! ' + error.message});
      });
  }
}

module.exports = PadController;
