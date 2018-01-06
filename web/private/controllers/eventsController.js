'use strict';

var config = require('../../config.js');
var DB = require('../services/database.js');

var EventsController = {}

EventsController.getEvents = function (req, res) {
  var offset = (req.query.offset) ? parseInt(req.query.offset) : 0;
  var lastID = (req.query.lastID) ? parseInt(req.query.lastID) : 0;
  var groupID = (req.query.groupID) ? parseInt(req.query.groupID) : 0;

  var where = {[DB.Op.and]: [
    {group_id: groupID},
    {id: {[DB.Op.gt]: lastID}}
  ]};
  
  DB.Event.findAll({limit: 25, where: where, offset: offset, order: [['time', 'DESC']]})
    .then(function (events) {
      res.json(events);
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue :' + error.message});
    });
}

module.exports = EventsController;
