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
  
  var getEvents = function (events) {
    var promises = []
    for (var i = 0; i < events.length; i++) {
      if (events[i].battle_id !== null) {
         promises[i] = DB.Battle.findOne({where: {id: events[i].battle_id}});
      } else if (events[i].idt_id !== null) {
         promises[i] = DB.IDT.findOne({where: {id: events[i].idt_id}});
      } else if (events[i].idc_id !== null) {
         promises[i] = DB.IDC.findOne({where: {id: events[i].idc_id}});
      } else if (events[i].piege_id !== null) {
         promises[i] = DB.Piege.findOne({where: {id: events[i].piege_id}});
      } else if (events[i].portal_id !== null) {
         promises[i] = DB.Portal.findOne({where: {id: events[i].portal_id}});
      } else if (events[i].cdm_id !== null) {
         promises[i] = DB.CDM.findOne({where: {id: events[i].cdm_id}});
      } else if (events[i].aa_id !== null) {
         promises[i] = DB.AA.findOne({where: {id: events[i].aa_id}});
      }
    }
    Promise.all(promises)
      .then(function (subevents) {
        for (var i = 0; i < subevents.length; i++) {
          events[i].dataValues.sub = subevents[i];
        }
        res.json(events);
      });
  };
 
  DB.Event.scope().findAll({limit: 25, where: where, offset: offset, order: [['time', 'DESC']]})
    .then(function (events) {
      getEvents(events);
    })
    .catch(function(error) {
      res.status(500).json({message: 'Une erreur est survenue :' + error.message});
    });
}

module.exports = EventsController;
