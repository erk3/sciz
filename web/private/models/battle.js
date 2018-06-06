'use strict'; 

var sequelize = require('sequelize');
var BattleTemplate = {};

/*
 * Definition
 */
BattleTemplate.name = 'Battle';
BattleTemplate.table = 'battles';

BattleTemplate.modelDefinition = {  
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
  att_troll_id: {type: sequelize.INTEGER},
  def_troll_id: {type: sequelize.INTEGER},
  att_mob_id: {type: sequelize.INTEGER},
  def_mob_id: {type: sequelize.INTEGER},
  type: {type: sequelize.STRING},
  subtype: {type: sequelize.STRING},
  att: {type: sequelize.INTEGER},
  esq: {type: sequelize.INTEGER},
  deg: {type: sequelize.INTEGER},
  arm: {type: sequelize.INTEGER},
  pv: {type: sequelize.INTEGER},
  vie: {type: sequelize.INTEGER},
  soin: {type: sequelize.INTEGER},
  blessure: {type: sequelize.INTEGER},
  sr: {type: sequelize.INTEGER},
  resi: {type: sequelize.INTEGER},
  capa_desc: {type: sequelize.STRING},
  capa_effet: {type: sequelize.STRING},
  capa_tour: {type: sequelize.INTEGER},
  resist: {type: sequelize.BOOLEAN},
  crit: {type: sequelize.BOOLEAN},
  perfect_dodge: {type: sequelize.BOOLEAN},
  dead: {type: sequelize.BOOLEAN},
  px: {type: sequelize.INTEGER},
  fatigue: {type: sequelize.INTEGER}
};

BattleTemplate.modelOptions = {
  name: {
    singular: 'battle',
    plural: 'battles'
  }
};

module.exports = BattleTemplate;
