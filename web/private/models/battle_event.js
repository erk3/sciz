'use strict'; 

var Sequelize = require('sequelize');

var db = require('../services/database.js');
var TrollModel = require ('./troll.js');
var MobModel = require ('./mob.js');

var modelDefinition = {  
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    allowNull: false
  },
  time: {type: Sequelize.DATE},
  att_troll_id: {type: Sequelize.INTEGER},
  def_troll_id: {type: Sequelize.INTEGER},
  att_mob_id: {type: Sequelize.INTEGER},
  def_mob_id: {type: Sequelize.INTEGER},
  flag_type: {type: Sequelize.STRING},
  type: {type: Sequelize.STRING},
  subtype: {type: Sequelize.STRING},
  att: {type: Sequelize.INTEGER},
  esq: {type: Sequelize.INTEGER},
  deg: {type: Sequelize.INTEGER},
  pv: {type: Sequelize.INTEGER},
  vie: {type: Sequelize.INTEGER},
  soin: {type: Sequelize.INTEGER},
  blessure: {type: Sequelize.INTEGER},
  sr: {type: Sequelize.INTEGER},
  resi: {type: Sequelize.INTEGER},
  capa_desc: {type: Sequelize.STRING},
  capa_effet: {type: Sequelize.STRING},
  capa_tour: {type: Sequelize.INTEGER}
};

var modelOptions = {
  defaultScope: {
    include: [
      {model: TrollModel, as: 'att_troll'},
      {model: TrollModel, as: 'def_troll'},
      {model: MobModel, as: 'att_mob'},
      {model: MobModel, as: 'def_mob'}
    ]
  }
};

var BattleEventModel = db.define('battle_events', modelDefinition, modelOptions);
BattleEventModel.belongsTo(TrollModel, {as: 'att_troll', foreignKey: 'att_troll_id', targetKey: 'id'});
BattleEventModel.belongsTo(TrollModel, {as: 'def_troll', foreignKey: 'def_troll_id', targetKey: 'id'});
BattleEventModel.belongsTo(MobModel, {as: 'att_mob', foreignKey: 'att_mob_id', targetKey: 'id'});
BattleEventModel.belongsTo(MobModel, {as: 'def_mob', foreignKey: 'def_mob_id', targetKey: 'id'});

module.exports = BattleEventModel;
