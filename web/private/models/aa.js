'use strict'; 

var sequelize = require('sequelize');
var AATemplate = {};

/*
 * Definition
 */
AATemplate.name = 'AA';
AATemplate.table = 'aas';

AATemplate.modelDefinition = {  
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
  troll_cible_id: {type: sequelize.INTEGER},
  niv: {type: sequelize.INTEGER},
  blessure: {type: sequelize.INTEGER},
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
  vue_max: {type: sequelize.INTEGER}
};

AATemplate.modelOptions = {
  name: {
    singular: 'aa',
    plural: 'aas'
  }
};

module.exports = AATemplate;
