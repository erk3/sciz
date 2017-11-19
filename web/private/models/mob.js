'use strict'; 

var sequelize = require('sequelize');
var MobTemplate = {};

/*
 * Methods
 */
MobTemplate.changeBlasonURL = function (mob) {
  if (mob && mob.metamob && mob.metamob.blason_url && !mob.metamob.blason_url) {
    mob.metamob.blason_url = 'http://blason.mountyhall.com/Blason_PJ/MyNameIsNobody.gif';
  }
  return mob;
};

/*
 * Definition
 */
MobTemplate.name = 'Mob';
MobTemplate.table = 'mobs';

MobTemplate.modelDefinition = {  
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
  metamob_id: {type: sequelize.INTEGER},
  nom: {type: sequelize.STRING},
  type: {type: sequelize.STRING},
  tag: {type: sequelize.STRING},
  age: {type: sequelize.STRING},
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
  vit_dep: {type: sequelize.STRING},
  att_dist: {type: sequelize.BOOLEAN},
  dla: {type: sequelize.STRING},
  tour_min: {type: sequelize.INTEGER},
  tour_max: {type: sequelize.INTEGER},
  chargement: {type: sequelize.STRING},
  bonus_malus:  {type: sequelize.STRING},
  portee_capa: {type: sequelize.STRING}
};

MobTemplate.modelOptions = {
  name: {
    singular: 'mob',
    plural: 'mobs'
  },
  hooks: {
    afterFind: MobTemplate.changeBlasonURL
  }
};

module.exports = MobTemplate;
