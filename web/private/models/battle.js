'use strict'; 

var sequelize = require('sequelize');
var TrollTemplate = require('./troll.js');
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
  par: {type: sequelize.INTEGER},
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
  dodge: {type: sequelize.BOOLEAN},
  perfect_dodge: {type: sequelize.BOOLEAN},
  parade: {type: sequelize.BOOLEAN},
  dead: {type: sequelize.BOOLEAN},
  px: {type: sequelize.INTEGER},
  rm: {type: sequelize.INTEGER},
  mm: {type: sequelize.INTEGER},
  fatigue: {type: sequelize.INTEGER},
  retraite: {type: sequelize.STRING},
  destab: {type: sequelize.INTEGER},
  stab: {type: sequelize.INTEGER}
};

BattleTemplate.modelOptions = {
  name: {
    singular: 'battle',
    plural: 'battles'
  },
  hooks: {
    afterFind: function (battle) {
      if (battle && battle.att_troll) {
        TrollTemplate.changeBlasonURL(battle.att_troll);
      }
      if (battle && battle.def_troll) {
        TrollTemplate.changeBlasonURL(battle.def_troll);
      }
    }
  }
};

module.exports = BattleTemplate;
