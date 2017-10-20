'use strict'; 

var Sequelize = require('sequelize');

var db = require('../services/database.js');
var MobModel = require('./mob.js');
var TrollModel = require('./troll.js');

var modelDefinition = {  
  id: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    allowNull: false
  },
  time: {type: Sequelize.DATE},
  troll_id: {type: Sequelize.INTEGER},
  mob_id: {type: Sequelize.INTEGER},
  comp_niv: {type: Sequelize.INTEGER},
  blessure: {type: Sequelize.INTEGER},
  niv_min: {type: Sequelize.INTEGER},
  niv_max: {type: Sequelize.INTEGER},
  pv_min: {type: Sequelize.INTEGER},
  pv_max: {type: Sequelize.INTEGER},
  att_min: {type: Sequelize.INTEGER},
  att_max: {type: Sequelize.INTEGER},
  esq_min: {type: Sequelize.INTEGER},
  esq_max: {type: Sequelize.INTEGER},
  deg_min: {type: Sequelize.INTEGER},
  deg_max: {type: Sequelize.INTEGER},
  reg_min: {type: Sequelize.INTEGER},
  reg_max: {type: Sequelize.INTEGER},
  arm_phy_min: {type: Sequelize.INTEGER},
  arm_phy_max: {type: Sequelize.INTEGER},
  vue_min: {type: Sequelize.INTEGER},
  vue_max: {type: Sequelize.INTEGER},
  capa_desc: {type: Sequelize.STRING},
  capa_effet: {type: Sequelize.STRING},
  capa_tour: {type: Sequelize.INTEGER},
  mm_min: {type: Sequelize.INTEGER},
  mm_max: {type: Sequelize.INTEGER},
  rm_min: {type: Sequelize.INTEGER},
  rm_max: {type: Sequelize.INTEGER},
  nb_att_tour: {type: Sequelize.INTEGER},
  vlc: {type: Sequelize.BOOLEAN},
  vit_dep: {type: Sequelize.STRING},
  att_dist: {type: Sequelize.BOOLEAN},
  dla: {type: Sequelize.STRING},
  tour_min: {type: Sequelize.INTEGER},
  tour_max: {type: Sequelize.INTEGER},
  chargement: {type: Sequelize.STRING},
  bonus_malus:  {type: Sequelize.STRING},
  portee_capa: {type: Sequelize.STRING}
};

var modelOptions = {
  defaultScope: {
    include: [
      {model: MobModel, as: 'mob'},
      {model: TrollModel, as: 'troll'}
    ]
  }
};

var CDMModel = db.define('cdms', modelDefinition, modelOptions);
CDMModel.belongsTo(MobModel, {as: 'mob', foreignKey: 'mob_id', targetKey: 'id'});
CDMModel.belongsTo(TrollModel, {as: 'troll', foreignKey: 'troll_id', targetKey: 'id'});

module.exports = CDMModel;
