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
  }
};

var EventModel = db.define('events', modelDefinition, modelOptions);
EventModel.belongsTo(BattleEventModel, {as: 'battle_event', foreignKey: 'battle_event_id', targetKey: 'id'});
EventModel.belongsTo(CDMModel, {as: 'cdm', foreignKey: 'cdm_id', targetKey: 'id'});
  
module.exports = EventModel;
