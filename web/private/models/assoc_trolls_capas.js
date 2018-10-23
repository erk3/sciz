'use strict'; 

var sequelize = require('sequelize');
var AssocTrollsCapasTemplate = {};

/*
 * Definition
 */
AssocTrollsCapasTemplate.name = 'AssocTrollsCapas';
AssocTrollsCapasTemplate.table = 'assoc_trolls_capas';

AssocTrollsCapasTemplate.modelDefinition = {  
  troll_id: {type: sequelize.INTEGER, primaryKey: true},
  metacapa_id: {type: sequelize.INTEGER, primaryKey: true},
  group_id: {type: sequelize.INTEGER, primaryKey: true},
  niv: {type: sequelize.INTEGER},
  percent: {type: sequelize.INTEGER},
  subtype: {type: sequelize.STRING},
  bonus: {type: sequelize.INTEGER}
};

AssocTrollsCapasTemplate.modelOptions = {
  name: {
    singular: 'assoc_trolls_capas',
    plural: 'assoc_trolls_capas'
  }
};

module.exports = AssocTrollsCapasTemplate;
