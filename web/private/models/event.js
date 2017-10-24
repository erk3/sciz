'use strict'; 

var Sequelize = require('sequelize');

var db = require('../services/database.js');
var BattleEventModel = require('./battle_event.js');
var CDMModel = require('./cdm.js');

var modelDefinition = {  
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    allowNull: false
  },
  notif: {type: Sequelize.STRING},
  notif_to_push: {type: Sequelize.BOOLEAN},
  type: {type: Sequelize.STRING},
  battle_event_id: {type: Sequelize.INTEGER},
  cdm_id: {type: Sequelize.INTEGER}
};

var modelOptions = {
  defaultScope: {
    include: [
      {model: BattleEventModel, as: 'battle_event'},
      {model: CDMModel, as: 'cdm'}
    ]
  },
  hooks: {
    afterFind: changeTrollsBlasonURL
  }
};

var EventModel = db.define('events', modelDefinition, modelOptions);
EventModel.belongsTo(BattleEventModel, {as: 'battle_event', foreignKey: 'battle_event_id', targetKey: 'id'});
EventModel.belongsTo(CDMModel, {as: 'cdm', foreignKey: 'cdm_id', targetKey: 'id'});

function changeTrollsBlasonURL(events) { 
  var metaChangeTrollBlasonURL = function (troll) {
    if (troll && troll.blason && troll.blason_url.startsWith('http://www.mountyhall.com/images/Blasons/Blason_PJ')) { 
    troll.blason_url = 'http://blason.mountyhall.com/Blason_PJ/' + troll.id;
    }
    return troll;
  };
  for (var e = 0; e < events.length; e++) {
    if (events[e].cdm && events[e].cdm.troll) {
      events[e].cdm.troll = metaChangeTrollBlasonURL(events[e].cdm.troll);
    }
    if (events[e].battle_event && events[e].battle_event.att_troll) {
      events[e].battle_event.att_troll = metaChangeTrollBlasonURL(events[e].battle_event.att_troll);
    }
    if (events[e].battle_event && events[e].battle_event.def_troll) {
      events[e].battle_event.def_troll = metaChangeTrollBlasonURL(events[e].battle_event.def_troll);
    }
  }
}
 
module.exports = EventModel;
