'use strict'; 

var sequelize = require('sequelize');
var ConfTemplate = {};

/*
 * Definition
 */
ConfTemplate.name = 'Conf';
ConfTemplate.table = 'confs';

ConfTemplate.modelDefinition = {  
  id: {
    type: sequelize.INTEGER,
    primaryKey: true,
    unique: 'UniqueKeyConstraint',
    allowNull: false
  },
  group_id: {
    type: sequelize.INTEGER,
    unique: 'UniqueKeyConstraint'
  },
  key: {type: sequelize.STRING},
  value: {type: sequelize.STRING},
  last_fetch: {type: sequelize.DATE}
};

ConfTemplate.modelOptions = {
  name: {
    singular: 'conf',
    plural: 'confs'
  }
};

module.exports = ConfTemplate;
