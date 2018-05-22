'use strict'; 

var sequelize = require('sequelize');
var TrollTemplate = require('./troll.js');
var EventTemplate = {};

/*
 * Definition
 */
EventTemplate.name = 'Event';
EventTemplate.table = 'events';

EventTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: 'PrimaryKeyConstraint',
    allowNull: false
  },
  group_id: {
    type: sequelize.INTEGER,
    primaryKey: 'PrimaryKeyConstraint',
    allowNull: false
  },
  time: {type: sequelize.DATE},
  notif: {type: sequelize.STRING},
  notif_to_push: {type: sequelize.BOOLEAN},
  type: {type: sequelize.STRING},
  battle_id: {type: sequelize.INTEGER},
  cdm_id: {type: sequelize.INTEGER},
  piege_id: {type: sequelize.INTEGER},
  idc_id: {type: sequelize.INTEGER},
  aa_id: {type: sequelize.INTEGER}
};

EventTemplate.modelOptions = {
  name: {
    singular: 'event',
    plural: 'events'
  },
  hooks: {
    afterFind: function (events) {
      for (var e = 0; e < events.length; e++) {
        if (events[e].cdm && events[e].cdm.troll) {
          events[e].cdm.troll = TrollTemplate.changeBlasonURL(events[e].cdm.troll);
        }
        if (events[e].aa && events[e].aa.troll && events[e].aa.troll_cible) {
          events[e].aa.troll = TrollTemplate.changeBlasonURL(events[e].aa.troll);
          events[e].aa.troll_cible = TrollTemplate.changeBlasonURL(events[e].aa.troll_cible);
        }
        if (events[e].idc && events[e].idc.troll) {
          events[e].idc.troll = TrollTemplate.changeBlasonURL(events[e].idc.troll);
        }
        if (events[e].piege && events[e].piege.troll) {
          events[e].piege.troll = TrollTemplate.changeBlasonURL(events[e].piege.troll);
        }
        if (events[e].portal && events[e].portal.troll) {
          events[e].portal.troll = TrollTemplate.changeBlasonURL(events[e].portal.troll);
        }
        if (events[e].battle && events[e].battle.att_troll) {
          events[e].battle.att_troll = TrollTemplate.changeBlasonURL(events[e].battle.att_troll);
        }
        if (events[e].battle && events[e].battle.def_troll) {
          events[e].battle.def_troll = TrollTemplate.changeBlasonURL(events[e].battle.def_troll);
        }
      } 
    }
  }
};

module.exports = EventTemplate;
