'use strict'; 

var sequelize = require('sequelize');
var CDMTemplate = {};

/*
 * Definition
 */
CDMTemplate.name = 'CDM';
CDMTemplate.table = 'cdms';

CDMTemplate.modelDefinition = {  
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
  troll_id: {type: sequelize.INTEGER},
  mob_id: {type: sequelize.INTEGER},
  comp_niv: {type: sequelize.INTEGER},
  blessure: {type: sequelize.INTEGER},
  niv_min: {type: sequelize.INTEGER},
  niv_max: {type: sequelize.INTEGER},
  pv_min: {type: sequelize.INTEGER},
  pv_max: {type: sequelize.INTEGER},
  att_min: {type: sequelize.INTEGER},
  att_max: {type: sequelize.INTEGER},
  esq_min: {type: sequelize.INTEGER},
  esq_max: {type: sequelize.INTEGER},
  deg_min: {type: sequelize.INTEGER},
  deg_max: {type: sequelize.INTEGER},
  reg_min: {type: sequelize.INTEGER},
  reg_max: {type: sequelize.INTEGER},
  arm_phy_min: {type: sequelize.INTEGER},
  arm_phy_max: {type: sequelize.INTEGER},
  arm_mag_min: {type: sequelize.INTEGER},
  arm_mag_max: {type: sequelize.INTEGER},
  vue_min: {type: sequelize.INTEGER},
  vue_max: {type: sequelize.INTEGER},
  capa_desc: {type: sequelize.STRING},
  capa_effet: {type: sequelize.STRING},
  capa_tour: {type: sequelize.INTEGER},
  mm_min: {type: sequelize.INTEGER},
  mm_max: {type: sequelize.INTEGER},
  rm_min: {type: sequelize.INTEGER},
  rm_max: {type: sequelize.INTEGER},
  nb_att_tour: {type: sequelize.INTEGER},
  vlc: {type: sequelize.BOOLEAN},
  voleur: {type: sequelize.BOOLEAN},
  vit_dep: {type: sequelize.STRING},
  att_dist: {type: sequelize.BOOLEAN},
  att_mag: {type: sequelize.BOOLEAN},
  dla: {type: sequelize.STRING},
  sang_froid: {type: sequelize.STRING},
  tour_min: {type: sequelize.INTEGER},
  tour_max: {type: sequelize.INTEGER},
  chargement: {type: sequelize.STRING},
  bonus_malus:  {type: sequelize.STRING},
  portee_capa: {type: sequelize.STRING}
};

CDMTemplate.modelOptions = {
  name: {
    singular: 'cdm',
    plural: 'cdms'
  }
};

module.exports = CDMTemplate;
